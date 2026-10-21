def migrate(cr, version):
    """Pasa la actividad económica única (Many2one) a la nueva tabla de actividades (Many2many)."""
    cr.execute("""
        SELECT 1 FROM information_schema.columns
        WHERE table_name = 'res_partner' AND column_name = 'actividad_economica_id'
    """)
    if not cr.fetchone():
        return

    cr.execute("""
        INSERT INTO res_partner_actividad_economica_rel (partner_id, actividad_id)
        SELECT id, actividad_economica_id FROM res_partner
        WHERE actividad_economica_id IS NOT NULL
        ON CONFLICT DO NOTHING
    """)
    cr.execute("""
        INSERT INTO res_partner_actividad_padre_rel (partner_id, padre_id)
        SELECT DISTINCT rel.partner_id, ae.actividad_padre_id
        FROM res_partner_actividad_economica_rel rel
        JOIN actividad_economica ae ON ae.id = rel.actividad_id
        WHERE ae.actividad_padre_id IS NOT NULL
        ON CONFLICT DO NOTHING
    """)
    cr.execute("ALTER TABLE res_partner DROP COLUMN IF EXISTS actividad_economica_id")
    cr.execute("ALTER TABLE res_partner DROP COLUMN IF EXISTS actividad_padre_id")
