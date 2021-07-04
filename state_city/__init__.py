# -*- coding: utf-8 -*-
from . import city

def post_init_hook(cr, registry):
    import os, csv
    from odoo.api import Environment, SUPERUSER_ID
     
    env = Environment(cr, SUPERUSER_ID, {})
    dir_path = os.path.dirname(os.path.realpath(__file__))
    
    with open(dir_path + '/res.state.city.csv', 'rt') as csvfile:
        city_values = []
        for row in csv.DictReader(csvfile, delimiter=',', quotechar='"'):
            city_values.append(cr.mogrify('(%s, %s, %s, %s)', (
                state_ids[row['state_id/id'].replace('state_city.', '')],
                row['code'],
                row['name'],
                row['kabupaten'].upper() == 'TRUE')).decode())
        cr.execute("""
        WITH insert_data AS (
            INSERT INTO res_state_city (state_id, code, name, kabupaten) VALUES %s RETURNING code, id)
        INSERT INTO ir_model_data (module, name, model, res_id) SELECT 'state_city', code, 'res.state.city', id FROM insert_data RETURNING name, res_id
        """ % ','.join(city_values))
        city_ids = dict(cr.fetchall())
    
    with open(dir_path + '/res.city.kecamatan.csv', 'rt') as csvfile:
        kecamatan_values = []
        for row in csv.DictReader(csvfile, delimiter=',', quotechar='"'):
            kecamatan_values.append(cr.mogrify('(%s, %s, %s)', (
                city_ids[row['city_id/id'].replace('state_city.', '')],
                row['code'],
                row['name'])).decode())
        cr.execute("""
        WITH insert_data AS (
            INSERT INTO res_city_kecamatan (city_id, code, name) VALUES %s RETURNING code, id)
        INSERT INTO ir_model_data (module, name, model, res_id) SELECT 'state_city', code, 'res.city.kecamatan', id FROM insert_data RETURNING name, res_id
        """ % ','.join(kecamatan_values))
        kecamatan_ids = dict(cr.fetchall())
        
    with open(dir_path + '/res.kecamatan.kelurahan.csv', 'rt') as csvfile:
        kelurahan_values = []
        for row in csv.DictReader(csvfile, delimiter=',', quotechar='"'):
            kelurahan_values.append(cr.mogrify('(%s, %s, %s, %s)', (
                kecamatan_ids[row['kecamatan_id/id'].replace('state_city.', '')],
                row['zip'],
                row['name'],
                row['desa'].upper() == 'TRUE')).decode())
        cr.execute("""
        WITH insert_data AS (
            INSERT INTO res_kecamatan_kelurahan (kecamatan_id, zip, name, desa) VALUES %s RETURNING id)
        INSERT INTO ir_model_data (module, name, model, res_id) SELECT 'state_city', CONCAt('res_kecamatan_kelurahan_',id::TEXT), 'res.kecamatan.kelurahan', id FROM insert_data
            
        """ % ','.join(kelurahan_values))
    
def uninstall_hook(cr, registry):
    cr.execute("""
        DELETE FROM res_country_state WHERE id IN (
            SELECT res_id FROM ir_model_data WHERE model = 'res.country.state' AND module = 'state_city');
        DELETE FROM ir_model_data WHERE model = 'res.country.state' AND module = 'state_city';
        
        DELETE FROM res_state_city WHERE id IN (
            SELECT res_id FROM ir_model_data WHERE model = 'res.state.city' AND module = 'state_city');
        DELETE FROM ir_model_data WHERE model = 'res.state.city' AND module = 'state_city';
        
        DELETE FROM res_city_kecamatan WHERE id IN (
            SELECT res_id FROM ir_model_data WHERE model = 'res.city.kecamatan' AND module = 'state_city');
        DELETE FROM ir_model_data WHERE model = 'res.city.kecamatan' AND module = 'state_city';
        
        DELETE FROM res_kecamatan_kelurahan WHERE id IN (
            SELECT res_id FROM ir_model_data WHERE model = 'res.kecamatan.kelurahan' AND module = 'state_city');
        DELETE FROM ir_model_data WHERE model = 'res.kecamatan.kelurahan' AND module = 'state_city';
    """)    
