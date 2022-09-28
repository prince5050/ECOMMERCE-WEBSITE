from django.contrib import admin
from django.urls import path
from .views import home, login, signup, tenders
from .views.home import Products
from .views.partners import Partners

# from .views import index, products, contact, sendmail, Signup, Login

urlpatterns = [
    path('', home.index, name='home'),
    path('index/', home.index, name='homepage'),
    path('products/', Products.as_view(), name='product_page'),
    path('products/category/<str:name>/', home.product_category),
    path('contact-us/', home.contact, name='contact'),
    path('products/<str:product_name>/<int:id>/', home.product_details, name='ProductDetails'),
    path('product-search/', home.product_search, name='product_search'),
    path('products/product-with-price/', home.product_with_price),
    path('products/product-without-price/', home.product_without_price),
    path('products/price-high-to-low/', home.price_high_to_low),
    path('products/price-low-to-high/', home.price_low_to_high),
    path('request-quote/', home.request_quote, name='quotation'),
    path('tenders/', tenders.Tenders.as_view(), name='tenders'),
    path('sendmail/', home.sendmail),
    path('quotation/', home.quotation),
    # path('signup1/', signup.Signup.as_view()),
    # path('login1/', login.Login.as_view(), name='login'),
    path('our-hubs/', home.our_hubs, name='hubs'),
    path('manufactureUnit/', home.manufactureUnit, name='manufactureUnit'),
    path('amphenolSensor/', home.amphenolSensor, name='amphenol'),
    path('partners/', Partners.as_view(), name='partners.html'),
    path('internship-application-form/', home.internship, name='internship_form'),
    path('latest-notification/', home.latest_notification),
    path('who-pre-qualification-cell/', home.pre_qualification, name='qualification'),
    path('brochures/', home.brochures, name='brochures'),
    path('amtz-schemes/', home.manufacturing_center, name='manufacturing'),
    path('innovation/', home.innovation, name='innovation'),
    path('preferential-market/', home.preferential_market),
    path('incentive-scheme/', home.incentive_scheme),
    path('RTI/', home.RTI),
    path('elderly-care-information-innovation-call/', home.elder_innovation),
    path('women-health-care-innovation-call/', home.women_innovation),
    path('biovalley-innovation-call-2022-Q3-for-biosensor-applications-artificial-intelligence-machine-learning-biotech-and-medtech-incubation-centre-in-healthtech-India/', home.biovalley_Innovation_Call),
    path('Auction-notice/', home.auction_notice),
    path('services/', home.services, name='services'),
    path('services/service-details/<str:name>/', home.services_details, name='service_details'),
    path('past-events/<int:id>/', home.past_events),
    path('past-event-details/<int:id>/', home.past_event_details),
    path('current-events/', home.ongoing_events),
    path('upcoming-events/', home.upcoming_events),
    path('service-request/', home.request_for_service),
    path('news/', home.news),
    path('amtz-videos/', home.our_videos),
    path('privacy-policy/', home.privacy),
    path('terms-conditions/', home.terms_condition),
    path('load_more/', home.load_more),
    path('load_more_product_with_price/', home.load_more_product_with_price),
    path('load_more_product_without_price/', home.load_more_product_without_price),
    path('load_more_product_price_high_to_low/', home.load_more_product_price_high_to_low),
    path('load_more_product_price_low_to_high/', home.load_more_product_price_low_to_high),
    path('dossiers/', home.dossiers),
    path('market-intelligence-and-trade-data/', home.market_intelligence),
    path('intellectual-property-publication/', home.intellectual_property),
    path('distributor-empanelment-form/', home.distributor_empanelment),
    path('skill-lync/', home.skill_lync),
    path('amtz-training-program/', home.training),
    path('v2home-privacy/', home.v2home_privacy),
    path('3d-bio-printing-innovation-call/', home.bio_printing_innovation_call),



]

