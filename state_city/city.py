# -*- coding: utf-8 -*-
from odoo import models,fields,api

class ResCompany(models.Model):
    _inherit = "res.company"
    
    city_id = fields.Many2one('res.state.city', 'Kabupaten')
    kecamatan_id = fields.Many2one('res.city.kecamatan', 'Kecamatan', domain=[('city_id', '=', 'city_id')])
    kelurahan_id = fields.Many2one('res.kecamatan.kelurahan', 'Kelurahan', domain="[('kecamatan_id','=',kecamatan_id)]")

class ResPartner(models.Model):
    _inherit = 'res.partner'
    
    state_id = fields.Many2one('res.country.state', "State", domain="[('country_id','=',country_id)]")
    city_id = fields.Many2one('res.state.city', 'Kabupaten', domain="[('state_id','=',state_id)]")
    kecamatan_id = fields.Many2one('res.city.kecamatan', 'Kecamatan', domain=[('city_id', '=', 'city_id')])
    kelurahan_id = fields.Many2one('res.kecamatan.kelurahan', 'Kelurahan', domain="[('kecamatan_id','=',kecamatan_id)]")
    
class Country(models.Model):
    _inherit = "res.country"
    
    state_ids = fields.One2many('res.country.state','country_id',"Propinsi")
    
class State(models.Model):
    _inherit = "res.country.state"
    
    code = fields.Char(size=255)
    city_ids = fields.One2many("res.state.city","state_id", "Kota/Kabupaten")
    
class City(models.Model):
    _name = "res.state.city"
    _description = 'Kota/Kabupaten'
    
    name = fields.Char("Nama Kota/Kabupaten")
    kabupaten = fields.Boolean('Kabupaten')
    code = fields.Char("Kode Kota")
    state_id = fields.Many2one('res.country.state', 'Propinsi', index=True)
    kecamatan_ids = fields.One2many('res.city.kecamatan', 'city_id','Kecamatan')
    
#     _sql_constraints = [('code_unique', 'unique(code)', "Kode kota harus unik")]
class Kecamatan(models.Model):
    _name = 'res.city.kecamatan'
    _description = 'Kecamatan'
    
    name = fields.Char('Nama Kecamatan')
    code = fields.Char('Kode Kecamatan')
    city_id = fields.Many2one('res.state.city', 'Kota/Kabupaten', index=True)
    kelurahan_ids = fields.One2many('res.kecamatan.kelurahan', 'kecamatan_id','Kelurahan')
    
class Kelurahan(models.Model):
    _name = 'res.kecamatan.kelurahan'
    _description = 'Kelurahan'
    
    name = fields.Char('Nama Kelurahan/Desa')
    zip = fields.Char('Kodepos')
    desa = fields.Boolean('Desa')
    kecamatan_id = fields.Many2one('res.city.kecamatan','Kecamatan', index=True)
    