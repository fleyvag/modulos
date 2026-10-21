# CRM - Seminarium (migrado a Odoo 17)

## ⚠️ Importante: esto NO trae lo que faltaba en el otro módulo

Revisé todo el código y **este módulo no contiene `sale_factor` ni
`pre_factor_sale_line_rel`** (las tablas que usa la columna "Descuento" del
reporte `sale_report_ventasxvendedor`). Es una funcionalidad distinta:
agrega líneas de producto a la oportunidad del CRM y permite convertirlas
en cotización. Probablemente exista un tercer módulo (quizá el que define
"sale_factor") que todavía no se ha subido.

## Qué se hizo en la migración/reorganización

- Estructura reorganizada al estándar de Odoo: `models/`, `views/`,
  `security/` (antes todo suelto en la raíz).
- `__openerp__.py` → `__manifest__.py`, versión `17.0.1.0.0`, agregado
  `license` (obligatorio desde v15) y `security/ir.model.access.csv`.
- `from openerp import ...` → `from odoo import ...` en todos los archivos.
- `import crm_lead` (import implícito relativo, solo válido en Python 2)
  → `from . import crm_lead` en los `__init__.py`. Sin este cambio el
  módulo ni siquiera cargaba en Python 3.
- Se quitó `@api.multi` (decorador eliminado hace muchas versiones; ahora
  los métodos son multi-record por defecto).
- `select=True` (atributo viejo de Many2one) → `index=True`.
- `product.uom` → `uom.uom` (el modelo se renombró en Odoo 13).
- `account.analytic.plan.instance` (modelo eliminado hace muchísimas
  versiones, de la época `account_analytic_plans` en OpenERP 7/8) →
  `account.analytic.account`, igual que se usa en el resto de tus módulos
  ya migrados.
- `self.product_id.name_template` → `self.product_id.product_tmpl_id.name`
  (forma explícita y segura de obtener el nombre de la plantilla desde una
  variante, en vez de depender de un campo relacionado que puede no
  existir según la versión).
- Se renombró `product_product.py` a `models/product_template.py`: el
  archivo se llamaba así pero la clase en realidad hereda
  `product.template`, no `product.product`.
- **Bug corregido:** la vista `view_form_product_product_peso_inherited`
  declaraba `model="product.product"` pero heredaba una vista que
  pertenece a `product.template` — eso Odoo lo rechaza por
  incompatibilidad de modelos. Se corrigió el `model` a `product.template`.
- **Bug corregido:** un `<record>` declaraba su propio id como
  `sale_crm.crm_case_form_view_oppor_inherit` (con el prefijo de OTRO
  módulo). Un módulo no debe declarar registros bajo el namespace de otro
  módulo; se corrigió a un id propio de este módulo
  (`crm_case_form_view_oppor_inherit_seminarium`).
- `<openerp>` → `<odoo>`, se quitó el widget `one2many_list` (no es un
  widget válido de Odoo, no hacía nada) y se limpió el bloque de vista
  comentado/muerto (`crm_case_tree_view_oppor_inherit`).
- Agregado `security/ir.model.access.csv` para `crm.lead.line` (modelo
  nuevo que no tenía permisos definidos).

## Campos que faltaban y tuve que agregar para que el módulo no se caiga

El código original **usaba** estos campos sin declararlos en ningún lado
del zip que me pasaste. Sin ellos, el módulo se habría caído al primer uso
(`AttributeError` o error de campo inexistente al hacer `create()`):

1. **`crm.lead.planned_revenue_usd`** y **`crm.lead.amount_of_quota`**: los
   usa `_onchange_crm_line`. Los agregué como campos `Float` simples en
   `models/crm_lead.py`.
2. **`sale.order.line.analytics_id`**: lo escriben `sale_order.py` y
   `crm_lead.py` al crear la cotización, pero nunca estaba declarado. Lo
   agregué en `models/sale_order_line.py`, apuntando a
   `account.analytic.account`.

Si en tu instalación original estos campos ya existían en OTRO módulo (con
otro nombre, otro modelo destino, o lógica adicional), avísame para
quitarlos de aquí y no duplicar/chocar con esa definición.

## Cosas que se quitaron por ser inválidas en v17

- `'lead_id': self.id` al crear la cotización: `sale.order` no tiene ni
  tuvo ese campo en este módulo.
- `'project_id': self.analytic_id.id` al crear la cotización: `project_id`
  ya no es la cuenta analítica de `sale.order` desde hace varias versiones
  (y en v17 el campo de cuenta analítica a nivel de cotización fue
  eliminado por completo). Si necesitas enlazar una cuenta analítica a
  toda la cotización, cuéntame cómo la usas y vemos cómo mapearla.

## Cosas que TÚ debes verificar antes de usarlo en producción

1. **Los xpaths de las vistas heredadas son frágiles:**
   - `//page[@string='Internal Notes']` (en la vista de `crm.crm_case_form_view_oppor`)
   - `//button[3]` (el 3er botón de `sale_crm.crm_case_form_view_oppor`,
     selector posicional que puede apuntar a un botón distinto en v17)

   Ambos hay que confirmarlos con el modo desarrollador contra tu base v17
   antes de instalar en producción.
2. Confirma si `sale_crm` sigue siendo el nombre del módulo puente
   CRM-Ventas en tu instalación v17 (lo asumí igual que en la versión
   original).
3. Revisa si el dominio del campo `product_id` en la línea de la
   oportunidad (`CUPO/DIA COMPLETO`, `CUPO/DIA 2`, `CUPO/DIA 1`) sigue
   reflejando los nombres de producto reales.
4. Prueba el módulo con datos reales de v17 — no se pudo probar contra una
   base de datos real en este proceso.
