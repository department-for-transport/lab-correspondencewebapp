from textblob import TextBlob
import numpy as np
import pandas as pd
import pickle

categories =['Active Accessible Travel',
'Airport Capacity Policy',
'Aviation Policy Delivery',
'Aviation Security Operations',
'Aviation Strategy and Consumers',
'Aviation, Maritime, Environment Statistics',
'Better Regulation and EU Transposition Policy',
'Buses and Taxis',
'Business Partner MPL',
'Cities, Places and Devolution',
'Corporate Finance Directorate',
'Driver and Vehicle Licensing Agency',
'Driver and Vehicle Standards Agency PQs',
'Driving Standards Agency PQs',
'EU Exit Team',
'Environmental Strategy',
'Financial Control and Governance',
'Franchise Design',
'Freight, Operator Licensing and Roadworthiness',
'Group Human Resources',
'Group Procurement and Estates',
'HR Operations',
'HR Policy',
'HS2 Property',
'High Speed Rail',
'High Speed Rail communications',
'Highways Agency',
'International Aviation, Safety and Environment',
'International Cooperation',
'International Vehicle Standards',
'Local Infrastructure',
'Low Carbon Fuels',
'Maritime And Coastguard Agency',
'Maritime Environment, Technology & Innovation',
'Maritime Infrastructure, People & Services',
'Northern Transport Programme and Delivery',
'Office for Low Emission Vehicles',
'PO P&C',
'Performance and Operations',
'Property',
'Rail Analysis',
'Rail Crossrail 2',
'Rail Funding and Fares',
'Rail Industry Competitiveness',
'Rail Intercity Express Programme',
'Rail Markets Strategy',
'Rail Network Rail Sponsorship',
'Rail Network Services-Intercity Team',
'Rail Network Services-London & South East',
'Rail Network Services-North',
'Rail Network Services-West',
'Rail Network Upgrades',
'Rail Passenger Services',
'Rail Sponsorship and Stakeholders',
'Rail Strategy Projects',
'Rail Thameslink Programme',
'Refranchising Programme Office',
'Regional Strategies London and South',
'Road Investment Strategy Client',
'Road Investment Strategy Futures',
'Road User Licensing, Insurance and Safety',
'Smart Ticketing',
'Statistics Travel and Safety',
'Statistics, Road and Freight',
'Traffic and Technology',
'Transport Appraisal and Strategic Modelling',
'low_group']


class SGDModel:

    def __init__(self):
        self.model = None
        self.categories = categories

    def load(self, path):
        with open('{}'.format(path), 'rb') as f:
            self.model = pickle.load(f)

    def predict(self, sentence_in):
        s = pd.DataFrame({'summary_cleaned': [sentence_in]})
        prediction = self.model.predict(s)
        return self.categories[int(prediction)]
