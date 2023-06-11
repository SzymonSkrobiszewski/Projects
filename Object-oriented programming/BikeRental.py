{
  "nbformat": 4,
  "nbformat_minor": 0,
  "metadata": {
    "colab": {
      "provenance": [],
      "authorship_tag": "ABX9TyMXSQcLFTht3vlZ4NJcXgzY",
      "include_colab_link": true
    },
    "kernelspec": {
      "name": "python3",
      "display_name": "Python 3"
    },
    "language_info": {
      "name": "python"
    }
  },
  "cells": [
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "view-in-github",
        "colab_type": "text"
      },
      "source": [
        "<a href=\"https://colab.research.google.com/github/SzymonSkrobiszewski/Project/blob/main/BikeRental.ipynb\" target=\"_parent\"><img src=\"https://colab.research.google.com/assets/colab-badge.svg\" alt=\"Open In Colab\"/></a>"
      ]
    },
    {
      "cell_type": "code",
      "source": [
        "from datetime import datetime, timedelta\n",
        "from dateutil import parser\n",
        "\n",
        "\n",
        "class BikeRental:\n",
        "    \n",
        "    def __init__(self, number_of_bike=0) -> None:\n",
        "        self._customers = {}\n",
        "        if isinstance(number_of_bike, int) and number_of_bike > 0:\n",
        "            self._number_of_bike = number_of_bike\n",
        "        else:\n",
        "            raise ValueError('The number of bikes should be positive.')\n",
        "\n",
        "    def display_number_of_available_bike(self):\n",
        "        return 'We currently have {} bikes.'.format(self._number_of_bike)\n",
        "    \n",
        "    def offers(self):\n",
        "        return 'Rent bikes on hourly basis $5 per hour.\\\n",
        "                \\nRent bikes on daily basis $20 per day.\\\n",
        "                \\nRent bikes on weekly basis $60 per week.\\\n",
        "                \\nFamily Rental, a promotion that can include from 3 to 5 Rentals with a discount of 30% of the total price'\n",
        "    \n",
        "    def validation(self, pesel, amount=1, time=1):\n",
        "        if len(str(pesel)) != 11 or not str(pesel).isnumeric():\n",
        "            raise ValueError('Enter a valid pesel number')\n",
        "        if amount > self._number_of_bike:\n",
        "            raise ValueError(f'We currently have {self._number_of_bike} bikes.')\n",
        "        elif time <= 0 or amount <= 0 or not (isinstance(time,  int) and isinstance(amount, int)):\n",
        "            raise ValueError('Time and amount of bikes should be positive integer numbers.')\n",
        "\n",
        "    def rent_bike_for_hours(self, pesel, amount=1, time=1):\n",
        "        self.validation(pesel, amount, time)\n",
        "        self._customers[str(pesel)] = ('hours', amount, time, datetime.now().strftime('%Y-%m-%d %H:%M:%S'))\n",
        "        expected_return_time = datetime.now() + timedelta(hours=time)\n",
        "        expected_return_time = expected_return_time.strftime('%Y-%m-%d %H:%M:%S')\n",
        "        print('The {} bike(s) has been rented, expected return time: {}'.format(amount, expected_return_time))\n",
        "        self._number_of_bike -= amount\n",
        "        return datetime.now().strftime('%Y-%m-%d %H:%M:%S')\n",
        "    \n",
        "    def rent_bike_for_days(self, pesel, amount=1, time=1):\n",
        "        self.validation(pesel, amount, time)\n",
        "        self._customers[str(pesel)] = ('days', amount, time, datetime.now().strftime('%Y-%m-%d %H:%M:%S'))\n",
        "        expected_return_time = datetime.now() + timedelta(days=time)\n",
        "        print('The {} bike(s) has been rented, expected return time: {}'.format(amount, expected_return_time))\n",
        "        self._number_of_bike -= amount\n",
        "        return datetime.now().strftime('%Y-%m-%d %H:%M:%S')\n",
        "\n",
        "    def rent_bike_for_weeks(self, pesel, amount=1, time=1):\n",
        "        self.validation(pesel, amount, time)\n",
        "        self._customers.update({pesel: ('weeks', amount, time, datetime.now().strftime('%Y-%m-%d %H:%M:%S'))})\n",
        "        expected_return_time = datetime.now() + timedelta(days=7 * time)\n",
        "        expected_return_time = expected_return_time.strftime('%Y-%m-%d %H:%M:%S')\n",
        "        print('The {} bike(s) has been rented, expected return time: {}'.format(amount, expected_return_time))\n",
        "        self._number_of_bike -= amount\n",
        "        return datetime.now().strftime('%Y-%m-%d %H:%M:%S')\n",
        "    \n",
        "    def calculating_the_bill(self, number_of_bikes, date_of_rental, the_amount_of_the_service, divider):\n",
        "        bill = 0\n",
        "        if 3 <= number_of_bikes <= 5:\n",
        "                bill = number_of_bikes * the_amount_of_the_service * \\\n",
        "                    round(abs(parser.parse(date_of_rental) - datetime.now()).seconds // divider)\n",
        "                self._number_of_bike += number_of_bikes\n",
        "                return 'The amount to be paid is {}$'.format(bill * 0.7)\n",
        "        else:\n",
        "            self._number_of_bike += number_of_bikes\n",
        "            return 'The amount to be paid is {}$'.format(bill)\n",
        "\n",
        "    def issue_bill(self, pesel):\n",
        "        try:\n",
        "            rental_option, number_of_bikes, rental_time, date_of_rental = self._customers[pesel]\n",
        "        except:\n",
        "            raise ValueError('Invalid Pesel')\n",
        "        with open('archieve_of_customers.txt', 'a') as file:\n",
        "            file.write('{} {} {} {}\\n'.format(rental_option, number_of_bikes, rental_time, date_of_rental))\n",
        "        if rental_option == 'hours':\n",
        "            del self._customers[pesel]\n",
        "            return self.calculating_the_bill(number_of_bikes, date_of_rental, 5, 3600)\n",
        "        elif rental_option == 'days':\n",
        "            del self._customers[pesel]\n",
        "            return self.calculating_the_bill(number_of_bikes, date_of_rental, 20, 86400)\n",
        "        else:\n",
        "            del self._customers[pesel]\n",
        "            return self.calculating_the_bill(number_of_bikes, date_of_rental, 60, 604800)\n"
      ],
      "metadata": {
        "id": "AmYjuaX1l6fY"
      },
      "execution_count": 1,
      "outputs": []
    }
  ]
}
