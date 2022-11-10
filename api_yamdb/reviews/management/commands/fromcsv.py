from django.core.management.base import BaseCommand

import pandas as pd
import glob


class Command(BaseCommand):
    def handle(self, *args, **options):
        all_files = glob.glob('*.csv')

        for filename in all_files:
            pd.read.csv(filename, index_col=None, header=0)
