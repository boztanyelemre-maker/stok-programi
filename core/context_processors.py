def sidebar_menu(request):
    menu = [
        {'title': 'Ana Sayfa', 'icon': 'bi-house-fill', 'url': 'dashboard', 'children': []},
        {'title': 'Proje', 'icon': 'bi-folder-fill', 'url': 'project_settings', 'children': []},
        {'title': 'Urunler', 'icon': 'bi-box-seam-fill', 'url': '', 'children': [
            {'title': 'Urun Listesi', 'url': 'product_list'},
            {'title': 'Kategoriler', 'url': 'category_list'},
        ]},
        {'title': 'Zimmet Islemleri', 'icon': 'bi-person-badge-fill', 'url': '', 'children': [
            {'title': 'Zimmet Listesi', 'url': 'assignment_list'},
            {'title': 'Yeni Zimmet', 'url': 'assignment_create'},
        ]},
        {'title': 'Stok', 'icon': 'bi-clipboard-data-fill', 'url': '', 'children': [
            {'title': 'Stok Giris Fisi', 'url': 'stock_entry'},
            {'title': 'Stok Cikis Fisi', 'url': 'stock_exit'},
            {'title': 'Transfer Fisi', 'url': 'stock_transfer'},
            {'title': 'Teslim Fisi', 'url': 'stock_delivery'},
            {'title': 'Stok Sayim', 'url': 'stock_count_form'},
            {'title': 'Sayim Listesi', 'url': 'stock_count_list'},
            {'title': 'Isyeri Stok Listesi', 'url': 'stock_list'},
            {'title': 'Stok Hareketleri', 'url': 'stock_movements'},
            {'title': 'Fis Listesi', 'url': 'stock_slip_list'},
            {'title': 'Kritik Stok', 'url': 'critical_stock'},
        ]},
        {'title': 'Stok Personeli', 'icon': 'bi-people-fill', 'url': 'user_list', 'children': []},
        {'title': 'Siparis', 'icon': 'bi-cart-fill', 'url': '', 'children': [
            {'title': 'Siparis Listesi', 'url': 'order_list'},
            {'title': 'Siparis Girisi', 'url': 'order_create'},
            {'title': 'Teslim Raporu', 'url': 'delivery_report'},
            {'title': 'Siparisteki Urunler', 'url': 'ordered_products'},
        ]},
        {'title': 'Demirbaslar', 'icon': 'bi-pc-display', 'url': '', 'children': [
            {'title': 'Demirbas Listesi', 'url': 'asset_list'},
            {'title': 'Demirbas Ekle', 'url': 'asset_create'},
        ]},
        {'title': 'Raporlar', 'icon': 'bi-graph-up', 'url': '', 'children': [
            {'title': 'Stok Raporu', 'url': 'stock_report'},
            {'title': 'Transfer Raporu', 'url': 'transfer_report'},
            {'title': 'Transfer Maliyet', 'url': 'transfer_cost_report'},
            {'title': 'Grup Raporu', 'url': 'group_report'},
            {'title': 'Proje Bazli Cikis', 'url': 'project_stock_report'},
        ]},
        {'title': 'Parametreler', 'icon': 'bi-gear-fill', 'url': '', 'children': [
            {'title': 'Proje Ayarlari', 'url': 'project_settings'},
            {'title': 'Lokasyon Ayarlari', 'url': 'location_settings'},
            {'title': 'Genel Ayarlar', 'url': 'general_settings'},
        ]},
    ]
    return {'sidebar_menu': menu}
