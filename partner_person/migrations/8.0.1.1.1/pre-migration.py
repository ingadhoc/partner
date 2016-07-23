# -*- encoding: utf-8 -*-


def migrate(cr, version):
    if not version:
        return
    cr.execute(
        'ALTER TABLE "res_partner" RENAME "birthdate" TO "birthdate_date"')
    # cr.execute('DROP INDEX IF EXISTS "%s_%s_index"'
    #            % (table, old))
    # rename_columns(cr, column_renames, version)

column_renames = {
    'product_template': [
        ('use_uom_prices', None)
    ]
}
