{
'name':'Kota',
'summary':'Adding city and district data',
'author':'Chairul Umam, Erlangga Indra Permana, & Fadhlullah',
'website':'https://erlaangga.github.io',
'category': 'Tools',
'depends':['base'],
'data':[
        'ir.model.access.csv',
        'city_view.xml',
        'res_view.xml',
        ],
'uninstall_hook': 'uninstall_hook',
'post_init_hook': 'post_init_hook',
}
