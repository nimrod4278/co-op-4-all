# Copyright 2021 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import logging
from core.services.bigqueryservice import BqService

class GoogleAdsService():
    '''Google Ads service that retrieves conversions for a specific
    Co-Op Configuration.

    Attributes:
        model_config: A mixed model representing a CoopConfig but including
        RetailerConfig params.
        bq_service: Service that handles all the BigQuery operations
    '''

    def __init__(self, model_config):
        self.model_config = model_config
        self.bq_service = BqService(model_config)

    def __get_formatted_conversions(self, sql_file):
        '''Formats the retrieved rows of the specified query by removing
        the column underscores to match the conversions format.

            Args:
            sql_file (str): The query to be executed.

            Returns:
                conversions (list): A list of formatted conversions
        '''
        conversions = self.bq_service.get_table_data(sql_file)
        for h in conversions.columns.values.tolist():
            conversions[h.replace("_", " ")] = conversions[h]
            del conversions[h]
        return conversions

    def get_conversions(self):
        '''Gets conversions as csv format to be sent to the manufacturer's
        Google Ads account.

            Returns:
                csv: A list of conversions as csv format with the required
                columns and format for Offline Conversions Import in Google Ads.
        '''
        try:
            conversions = self.__get_formatted_conversions('sql/get_google_ads_conversions.sql')
            csv = conversions.to_csv(sep=',', index=False, encoding='utf-8')
            return csv
        except Exception as error:
            logging.error(f'GoogleAdsService - get_conversions - Error getting the conversions \
             for the Co-Op Config { self.model_config["name"] } Error: { str(error) }')
        return None
