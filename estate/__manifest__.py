{
    "name": "Real Estate",
    "depends": [
    ],
    "data": [
        "security/ir.model.access.csv",  # CSV and XML files are loaded at the same place
        "views/estate_property_views.xml",  # Views are data too
        "views/estate_property_type_views.xml",
        "views/estate_property_tags_views.xml",
        "views/estate_menus.xml",
        "views/estate_property_offer_views.xml",
        "views/res_users_views.xml",
    #     "data/master_data.xml",  # Split the data in multiple files depending on the model
    ],
    "demo": [
        "demo/demo_data.xml",
    ],
    "application": True,
}
