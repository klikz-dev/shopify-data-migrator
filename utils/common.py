import re
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
import pycountry
import phonenumbers
from phonenumbers import geocoder, PhoneNumberFormat

COUNTRY_DICT = [
    {
        "worldbase-code": "034",
        "worldbase-char": "AA",
        "country-name": "Aruba",
        "iso-digit": "533",
        "iso-char": "ABW",
        "iso-char2": "AW",
    },

    {
        "worldbase-code": "005",
        "worldbase-char": "AF",
        "country-name": "Afghanistan",
        "iso-digit": "004",
        "iso-char": "AFG",
        "iso-char2": "AF",
    },

    {
        "worldbase-code": "025",
        "worldbase-char": "AO",
        "country-name": "Angola",
        "iso-digit": "024",
        "iso-char": "AGO",
        "iso-char2": "AO",
    },

    {
        "worldbase-code": "027",
        "worldbase-char": "AL",
        "country-name": "Anguilla",
        "iso-digit": "660",
        "iso-char": "AIA",
        "iso-char2": "AI",
    },

    {
        "worldbase-code": "009",
        "worldbase-char": "AB",
        "country-name": "Albania",
        "iso-digit": "008",
        "iso-char": "ALB",
        "iso-char2": "AL",
    },

    {
        "worldbase-code": "021",
        "worldbase-char": "AN",
        "country-name": "Andorra",
        "iso-digit": "020",
        "iso-char": "AND",
        "iso-char2": "AD",
    },

    {
        "worldbase-code": "525",
        "worldbase-char": "NA",
        "country-name": "Netherlands Antilles",
        "iso-digit": "530",
        "iso-char": "ANT",
        "iso-char2": "AN",
    },

    {
        "worldbase-code": "777",
        "worldbase-char": "UA",
        "country-name": "United Arab Emirates",
        "iso-digit": "784",
        "iso-char": "ARE",
        "iso-char2": "AE",
    },

    {
        "worldbase-code": "898",
        "worldbase-char": "XA",
        "country-name": "United Arab Emirates",
        "iso-digit": "784",
        "iso-char": "ARE",
        "iso-char2": "AE",
    },

    {
        "worldbase-code": "897",
        "worldbase-char": "XB",
        "country-name": "United Arab Emirates",
        "iso-digit": "784",
        "iso-char": "ARE",
        "iso-char2": "AE",
    },

    {
        "worldbase-code": "917",
        "worldbase-char": "XD",
        "country-name": "United Arab Emirates",
        "iso-digit": "784",
        "iso-char": "ARE",
        "iso-char2": "AE",
    },

    {
        "worldbase-code": "918",
        "worldbase-char": "XF",
        "country-name": "United Arab Emirates",
        "iso-digit": "784",
        "iso-char": "ARE",
        "iso-char2": "AE",
    },

    {
        "worldbase-code": "899",
        "worldbase-char": "XL",
        "country-name": "United Arab Emirates",
        "iso-digit": "784",
        "iso-char": "ARE",
        "iso-char2": "AE",
    },

    {
        "worldbase-code": "942",
        "worldbase-char": "XR",
        "country-name": "United Arab Emirates",
        "iso-digit": "784",
        "iso-char": "ARE",
        "iso-char2": "AE",
    },

    {
        "worldbase-code": "943",
        "worldbase-char": "XS",
        "country-name": "United Arab Emirates",
        "iso-digit": "784",
        "iso-char": "ARE",
        "iso-char2": "AE",
    },

    {
        "worldbase-code": "952",
        "worldbase-char": "XU",
        "country-name": "United Arab Emirates",
        "iso-digit": "784",
        "iso-char": "ARE",
        "iso-char2": "AE",
    },

    {
        "worldbase-code": "33",
        "worldbase-char": "AR",
        "country-name": "Argentina",
        "iso-digit": "032",
        "iso-char": "ARG",
        "iso-char2": "AR",
    },

    {
        "worldbase-code": "900",
        "worldbase-char": "AM",
        "country-name": "Armenia",
        "iso-digit": "051",
        "iso-char": "ARM",
        "iso-char2": "AM",
    },

    {
        "worldbase-code": "017",
        "worldbase-char": "AS",
        "country-name": "American Samoa",
        "iso-digit": "016",
        "iso-char": "ASM",
        "iso-char2": "AS",
    },

    {
        "worldbase-code": "000",
        "worldbase-char": "000",
        "country-name": "Antarctica",
        "iso-digit": "010",
        "iso-char": "ATA",
        "iso-char2": "AQ",
    },

    {
        "worldbase-code": "000",
        "worldbase-char": "000",
        "country-name": "French Southern Territories",
        "iso-digit": "260",
        "iso-char": "ATF",
        "iso-char2": "TF",
    },

    {
        "worldbase-code": "028",
        "worldbase-char": "AD",
        "country-name": "Antigua and Barbuda",
        "iso-digit": "028",
        "iso-char": "ATG",
        "iso-char2": "AG",
    },

    {
        "worldbase-code": "37",
        "worldbase-char": "AU",
        "country-name": "Australia",
        "iso-digit": "36",
        "iso-char": "AUS",
        "iso-char2": "AU",
    },

    {
        "worldbase-code": "41",
        "worldbase-char": "OS",
        "country-name": "Austria",
        "iso-digit": "40",
        "iso-char": "AUT",
        "iso-char2": "AT",
    },

    {
        "worldbase-code": "905",
        "worldbase-char": "JZ",
        "country-name": "Azerbaijan",
        "iso-digit": "031",
        "iso-char": "AZE",
        "iso-char2": "AZ",
    },

    {
        "worldbase-code": "113",
        "worldbase-char": "BD",
        "country-name": "Burundi",
        "iso-digit": "108",
        "iso-char": "BDI",
        "iso-char2": "BI",
    },

    {
        "worldbase-code": "69",
        "worldbase-char": "BL",
        "country-name": "Belgium",
        "iso-digit": "056",
        "iso-char": "BEL",
        "iso-char2": "BE",
    },

    {
        "worldbase-code": "072",
        "worldbase-char": "BN",
        "country-name": "Benin",
        "iso-digit": "204",
        "iso-char": "BEN",
        "iso-char2": "BJ",
    },

    {
        "worldbase-code": "101",
        "worldbase-char": "BF",
        "country-name": "Burkina Faso",
        "iso-digit": "854",
        "iso-char": "BFA",
        "iso-char2": "BF",
    },

    {
        "worldbase-code": "61",
        "worldbase-char": "BA",
        "country-name": "Bangladesh",
        "iso-digit": "050",
        "iso-char": "BGD",
        "iso-char2": "BD",
    },

    {
        "worldbase-code": "100",
        "worldbase-char": "BU",
        "country-name": "Bulgaria",
        "iso-digit": "100",
        "iso-char": "BGR",
        "iso-char2": "BG",
    },

    {
        "worldbase-code": "53",
        "worldbase-char": "BR",
        "country-name": "Bahrain",
        "iso-digit": "048",
        "iso-char": "BHR",
        "iso-char2": "BH",
    },

    {
        "worldbase-code": "049",
        "worldbase-char": "BH",
        "country-name": "Bahamas",
        "iso-digit": "044",
        "iso-char": "BHS",
        "iso-char2": "BS",
    },

    {
        "worldbase-code": "910",
        "worldbase-char": "BS",
        "country-name": "Bosnia and Herzegovina",
        "iso-digit": "070",
        "iso-char": "BIH",
        "iso-char2": "BA",
    },

    {
        "worldbase-code": "915",
        "worldbase-char": "BY",
        "country-name": "Belarus",
        "iso-digit": "112",
        "iso-char": "BLR",
        "iso-char2": "BY",
    },

    {
        "worldbase-code": "071",
        "worldbase-char": "BG",
        "country-name": "Belize",
        "iso-digit": "084",
        "iso-char": "BLZ",
        "iso-char2": "BZ",
    },

    {
        "worldbase-code": "073",
        "worldbase-char": "BE",
        "country-name": "Bermuda",
        "iso-digit": "060",
        "iso-char": "BMU",
        "iso-char2": "BM",
    },

    {
        "worldbase-code": "81",
        "worldbase-char": "BO",
        "country-name": "Bolivia",
        "iso-digit": "068",
        "iso-char": "BOL",
        "iso-char2": "BO",
    },

    {
        "worldbase-code": "089",
        "worldbase-char": "BZ",
        "country-name": "Brazil",
        "iso-digit": "076",
        "iso-char": "BRA",
        "iso-char2": "BR",
    },

    {
        "worldbase-code": "065",
        "worldbase-char": "BB",
        "country-name": "Barbados",
        "iso-digit": "052",
        "iso-char": "BRB",
        "iso-char2": "BB",
    },

    {
        "worldbase-code": "096",
        "worldbase-char": "BI",
        "country-name": "Brunei Darussalam",
        "iso-digit": "096",
        "iso-char": "BRN",
        "iso-char2": "BN",
    },

    {
        "worldbase-code": "077",
        "worldbase-char": "BT",
        "country-name": "Bhutan",
        "iso-digit": "064",
        "iso-char": "BTN",
        "iso-char2": "BT",
    },

    {
        "worldbase-code": "000",
        "worldbase-char": "000",
        "country-name": "Bouvet Island",
        "iso-digit": "074",
        "iso-char": "BVT",
        "iso-char2": "BV",
    },

    {
        "worldbase-code": "085",
        "worldbase-char": "BW",
        "country-name": "Botswana",
        "iso-digit": "072",
        "iso-char": "BWA",
        "iso-char2": "BW",
    },

    {
        "worldbase-code": "141",
        "worldbase-char": "CE",
        "country-name": "Central African Republic",
        "iso-digit": "140",
        "iso-char": "CAF",
        "iso-char2": "CF",
    },

    {
        "worldbase-code": "121",
        "worldbase-char": "CA",
        "country-name": "Canada",
        "iso-digit": "124",
        "iso-char": "CAN",
        "iso-char2": "CA",
    },

    {
        "worldbase-code": "000",
        "worldbase-char": "000",
        "country-name": "Cocos (Keeling) Islands",
        "iso-digit": "166",
        "iso-char": "CCK",
        "iso-char2": "CC",
    },

    {
        "worldbase-code": "721",
        "worldbase-char": "CH",
        "country-name": "Switzerland",
        "iso-digit": "756",
        "iso-char": "CHE",
        "iso-char2": "CH",
    },

    {
        "worldbase-code": "153",
        "worldbase-char": "CL",
        "country-name": "Chile",
        "iso-digit": "152",
        "iso-char": "CHL",
        "iso-char2": "CL",
    },

    {
        "worldbase-code": "157",
        "worldbase-char": "CP",
        "country-name": "China",
        "iso-digit": "156",
        "iso-char": "CHN",
        "iso-char2": "CN",
    },

    {
        "worldbase-code": "361",
        "worldbase-char": "IV",
        "country-name": "Cote d'Ivoire",
        "iso-digit": "384",
        "iso-char": "CIV",
        "iso-char2": "CI",
    },

    {
        "worldbase-code": "117",
        "worldbase-char": "CM",
        "country-name": "Cameroon",
        "iso-digit": "120",
        "iso-char": "CMR",
        "iso-char2": "CM",
    },

    {
        "worldbase-code": "865",
        "worldbase-char": "ZR",
        "country-name": "Congo, The Democratic Republic ofÂ000",
        "iso-digit": "180",
        "iso-char": "COD",
        "iso-char2": "CD",
    },

    {
        "worldbase-code": "173",
        "worldbase-char": "CQ",
        "country-name": "Congo",
        "iso-digit": "178",
        "iso-char": "COG",
        "iso-char2": "CG",
    },

    {
        "worldbase-code": "175",
        "worldbase-char": "CK",
        "country-name": "Cook Islands",
        "iso-digit": "184",
        "iso-char": "COK",
        "iso-char2": "CK",
    },

    {
        "worldbase-code": "165",
        "worldbase-char": "CB",
        "country-name": "Colombia",
        "iso-digit": "170",
        "iso-char": "COL",
        "iso-char2": "CO",
    },

    {
        "worldbase-code": "169",
        "worldbase-char": "CO",
        "country-name": "Comoros",
        "iso-digit": "174",
        "iso-char": "COM",
        "iso-char2": "KM",
    },

    {
        "worldbase-code": "127",
        "worldbase-char": "CV",
        "country-name": "Cape Verde",
        "iso-digit": "132",
        "iso-char": "CPV",
        "iso-char2": "CV",
    },

    {
        "worldbase-code": "177",
        "worldbase-char": "CC",
        "country-name": "Costa Rica",
        "iso-digit": "188",
        "iso-char": "CRI",
        "iso-char2": "CR",
    },

    {
        "worldbase-code": "181",
        "worldbase-char": "CU",
        "country-name": "Cuba",
        "iso-digit": "192",
        "iso-char": "CUB",
        "iso-char2": "CU",
    },

    {
        "worldbase-code": "916",
        "worldbase-char": "CX",
        "country-name": "Christmas Island",
        "iso-digit": "162",
        "iso-char": "CXR",
        "iso-char2": "CX",
    },

    {
        "worldbase-code": "131",
        "worldbase-char": "CI",
        "country-name": "Cayman Islands",
        "iso-digit": "136",
        "iso-char": "CYM",
        "iso-char2": "KY",
    },

    {
        "worldbase-code": "763",
        "worldbase-char": "CN",
        "country-name": "Cyprus",
        "iso-digit": "196",
        "iso-char": "CYP",
        "iso-char2": "CY",
    },

    {
        "worldbase-code": "185",
        "worldbase-char": "CY",
        "country-name": "Cyprus",
        "iso-digit": "196",
        "iso-char": "CYP",
        "iso-char2": "CY",
    },

    {
        "worldbase-code": "190",
        "worldbase-char": "XC",
        "country-name": "Czech Republic",
        "iso-digit": "203",
        "iso-char": "CZE",
        "iso-char2": "CZ",
    },

    {
        "worldbase-code": "269",
        "worldbase-char": "DE",
        "country-name": "Germany",
        "iso-digit": "276",
        "iso-char": "DEU",
        "iso-char2": "DE",
    },

    {
        "worldbase-code": "198",
        "worldbase-char": "DJ",
        "country-name": "Djibouti",
        "iso-digit": "262",
        "iso-char": "DJI",
        "iso-char2": "DJ",
    },

    {
        "worldbase-code": "199",
        "worldbase-char": "DO",
        "country-name": "Dominica",
        "iso-digit": "212",
        "iso-char": "DMA",
        "iso-char2": "DM",
    },

    {
        "worldbase-code": "197",
        "worldbase-char": "DK",
        "country-name": "Denmark",
        "iso-digit": "208",
        "iso-char": "DNK",
        "iso-char2": "DK",
    },

    {
        "worldbase-code": "201",
        "worldbase-char": "DR",
        "country-name": "Dominican Republic",
        "iso-digit": "214",
        "iso-char": "DOM",
        "iso-char2": "DO",
    },

    {
        "worldbase-code": "013",
        "worldbase-char": "AG",
        "country-name": "Algeria",
        "iso-digit": "012",
        "iso-char": "DZA",
        "iso-char2": "DZ",
    },

    {
        "worldbase-code": "209",
        "worldbase-char": "EC",
        "country-name": "Ecuador",
        "iso-digit": "218",
        "iso-char": "ECU",
        "iso-char2": "EC",
    },

    {
        "worldbase-code": "29",
        "worldbase-char": "EG",
        "country-name": "Egypt",
        "iso-digit": "818",
        "iso-char": "EGY",
        "iso-char2": "EG",
    },

    {
        "worldbase-code": "919",
        "worldbase-char": "ER",
        "country-name": "Eritrea",
        "iso-digit": "232",
        "iso-char": "ERI",
        "iso-char2": "ER",
    },

    {
        "worldbase-code": "000",
        "worldbase-char": "000",
        "country-name": "Western Sahara",
        "iso-digit": "732",
        "iso-char": "ESH",
        "iso-char2": "EH",
    },

    {
        "worldbase-code": "693",
        "worldbase-char": "ES",
        "country-name": "Spain",
        "iso-digit": "724",
        "iso-char": "ESP",
        "iso-char2": "ES",
    },

    {
        "worldbase-code": "219",
        "worldbase-char": "EO",
        "country-name": "Estonia",
        "iso-digit": "233",
        "iso-char": "EST",
        "iso-char2": "EE",
    },

    {
        "worldbase-code": "221",
        "worldbase-char": "ET",
        "country-name": "Ethiopia",
        "iso-digit": "231",
        "iso-char": "ETH",
        "iso-char2": "ET",
    },

    {
        "worldbase-code": "237",
        "worldbase-char": "SF",
        "country-name": "Finland",
        "iso-digit": "246",
        "iso-char": "FIN",
        "iso-char2": "FI",
    },

    {
        "worldbase-code": "233",
        "worldbase-char": "FJ",
        "country-name": "Fiji",
        "iso-digit": "242",
        "iso-char": "FJI",
        "iso-char2": "FJ",
    },

    {
        "worldbase-code": "229",
        "worldbase-char": "FA",
        "country-name": "Falkland Islands (Malvinas)",
        "iso-digit": "238",
        "iso-char": "FLK",
        "iso-char2": "FK",
    },

    {
        "worldbase-code": "241",
        "worldbase-char": "FR",
        "country-name": "France",
        "iso-digit": "250",
        "iso-char": "FRA",
        "iso-char2": "FR",
    },

    {
        "worldbase-code": "225",
        "worldbase-char": "FO",
        "country-name": "Faroe Islands",
        "iso-digit": "234",
        "iso-char": "FRO",
        "iso-char2": "FO",
    },

    {
        "worldbase-code": "135",
        "worldbase-char": "CR",
        "country-name": "Micronesia, Federated States of",
        "iso-digit": "583",
        "iso-char": "FSM",
        "iso-char2": "FM",
    },

    {
        "worldbase-code": "491",
        "worldbase-char": "MR",
        "country-name": "Micronesia, Federated States of",
        "iso-digit": "583",
        "iso-char": "FSM",
        "iso-char2": "FM",
    },

    {
        "worldbase-code": "253",
        "worldbase-char": "GA",
        "country-name": "Gabon",
        "iso-digit": "266",
        "iso-char": "GAB",
        "iso-char2": "GA",
    },

    {
        "worldbase-code": "785",
        "worldbase-char": "EN",
        "country-name": "United Kingdom",
        "iso-digit": "826",
        "iso-char": "GBR",
        "iso-char2": "GB",
    },

    {
        "worldbase-code": "793",
        "worldbase-char": "ND",
        "country-name": "United Kingdom",
        "iso-digit": "826",
        "iso-char": "GBR",
        "iso-char2": "GB",
    },

    {
        "worldbase-code": "797",
        "worldbase-char": "SC",
        "country-name": "United Kingdom",
        "iso-digit": "826",
        "iso-char": "GBR",
        "iso-char2": "GB",
    },

    {
        "worldbase-code": "801",
        "worldbase-char": "WA",
        "country-name": "United Kingdom",
        "iso-digit": "826",
        "iso-char": "GBR",
        "iso-char2": "GB",
    },

    {
        "worldbase-code": "000",
        "worldbase-char": "000",
        "country-name": "United Kingdom",
        "iso-digit": "826",
        "iso-char": "GBR",
        "iso-char2": "GB",
    },

    {
        "worldbase-code": "920",
        "worldbase-char": "GE",
        "country-name": "Georgia",
        "iso-digit": "268",
        "iso-char": "GEO",
        "iso-char2": "GE",
    },

    {
        "worldbase-code": "273",
        "worldbase-char": "GH",
        "country-name": "Ghana",
        "iso-digit": "288",
        "iso-char": "GHA",
        "iso-char2": "GH",
    },

    {
        "worldbase-code": "277",
        "worldbase-char": "GI",
        "country-name": "Gibraltar",
        "iso-digit": "292",
        "iso-char": "GIB",
        "iso-char2": "GI",
    },

    {
        "worldbase-code": "305",
        "worldbase-char": "GN",
        "country-name": "Guinea",
        "iso-digit": "324",
        "iso-char": "GIN",
        "iso-char2": "GN",
    },

    {
        "worldbase-code": "293",
        "worldbase-char": "GU",
        "country-name": "Guadeloupe",
        "iso-digit": "312",
        "iso-char": "GLP",
        "iso-char2": "GP",
    },

    {
        "worldbase-code": "261",
        "worldbase-char": "GB",
        "country-name": "Gambia",
        "iso-digit": "270",
        "iso-char": "GMB",
        "iso-char2": "GM",
    },

    {
        "worldbase-code": "303",
        "worldbase-char": "GS",
        "country-name": "Guinea-Bissau",
        "iso-digit": "624",
        "iso-char": "GNB",
        "iso-char2": "GW",
    },

    {
        "worldbase-code": "217",
        "worldbase-char": "EQ",
        "country-name": "Equatorial Guinea",
        "iso-digit": "226",
        "iso-char": "GNQ",
        "iso-char2": "GQ",
    },

    {
        "worldbase-code": "285",
        "worldbase-char": "GR",
        "country-name": "Greece",
        "iso-digit": "300",
        "iso-char": "GRC",
        "iso-char2": "GR",
    },

    {
        "worldbase-code": "291",
        "worldbase-char": "GG",
        "country-name": "Grenada",
        "iso-digit": "308",
        "iso-char": "GRD",
        "iso-char2": "GD",
    },

    {
        "worldbase-code": "289",
        "worldbase-char": "GL",
        "country-name": "Greenland",
        "iso-digit": "304",
        "iso-char": "GRL",
        "iso-char2": "GL",
    },

    {
        "worldbase-code": "301",
        "worldbase-char": "GT",
        "country-name": "Guatemala",
        "iso-digit": "320",
        "iso-char": "GTM",
        "iso-char2": "GT",
    },

    {
        "worldbase-code": "245",
        "worldbase-char": "FG",
        "country-name": "French Guiana",
        "iso-digit": "254",
        "iso-char": "GUF",
        "iso-char2": "GF",
    },

    {
        "worldbase-code": "297",
        "worldbase-char": "GM",
        "country-name": "Guam",
        "iso-digit": "316",
        "iso-char": "GUM",
        "iso-char2": "GU",
    },

    {
        "worldbase-code": "309",
        "worldbase-char": "GY",
        "country-name": "Guyana",
        "iso-digit": "328",
        "iso-char": "GUY",
        "iso-char2": "GY",
    },

    {
        "worldbase-code": "321",
        "worldbase-char": "HK",
        "country-name": "Hong Kong",
        "iso-digit": "344",
        "iso-char": "HKG",
        "iso-char2": "HK",
    },

    {
        "worldbase-code": "000",
        "worldbase-char": "000",
        "country-name": "Heard and Mc Donald Islands",
        "iso-digit": "334",
        "iso-char": "HMD",
        "iso-char2": "HM",
    },

    {
        "worldbase-code": "317",
        "worldbase-char": "HO",
        "country-name": "Honduras",
        "iso-digit": "340",
        "iso-char": "HND",
        "iso-char2": "HN",
    },

    {
        "worldbase-code": "179",
        "worldbase-char": "ZC",
        "country-name": "Croatia",
        "iso-digit": "191",
        "iso-char": "HRV",
        "iso-char2": "HR",
    },

    {
        "worldbase-code": "313",
        "worldbase-char": "HA",
        "country-name": "Haiti",
        "iso-digit": "332",
        "iso-char": "HTI",
        "iso-char2": "HT",
    },

    {
        "worldbase-code": "325",
        "worldbase-char": "HU",
        "country-name": "Hungary",
        "iso-digit": "348",
        "iso-char": "HUN",
        "iso-char2": "HU",
    },

    {
        "worldbase-code": "337",
        "worldbase-char": "ID",
        "country-name": "Indonesia",
        "iso-digit": "360",
        "iso-char": "IDN",
        "iso-char2": "ID",
    },

    {
        "worldbase-code": "333",
        "worldbase-char": "IN",
        "country-name": "India",
        "iso-digit": "356",
        "iso-char": "IND",
        "iso-char2": "IN",
    },

    {
        "worldbase-code": "000",
        "worldbase-char": "000",
        "country-name": "British Indian Ocean Territory",
        "iso-digit": "086",
        "iso-char": "IOT",
        "iso-char2": "IO",
    },

    {
        "worldbase-code": "349",
        "worldbase-char": "IR",
        "country-name": "Ireland",
        "iso-digit": "372",
        "iso-char": "IRL",
        "iso-char2": "IE",
    },

    {
        "worldbase-code": "341",
        "worldbase-char": "IA",
        "country-name": "Iran, Islamic Republic of",
        "iso-digit": "364",
        "iso-char": "IRN",
        "iso-char2": "IR",
    },

    {
        "worldbase-code": "345",
        "worldbase-char": "IQ",
        "country-name": "Iraq",
        "iso-digit": "368",
        "iso-char": "IRQ",
        "iso-char2": "IQ",
    },

    {
        "worldbase-code": "329",
        "worldbase-char": "IC",
        "country-name": "Iceland",
        "iso-digit": "352",
        "iso-char": "ISL",
        "iso-char2": "IS",
    },

    {
        "worldbase-code": "353",
        "worldbase-char": "IS",
        "country-name": "Israel",
        "iso-digit": "376",
        "iso-char": "ISR",
        "iso-char2": "IL",
    },

    {
        "worldbase-code": "357",
        "worldbase-char": "IT",
        "country-name": "Italy",
        "iso-digit": "380",
        "iso-char": "ITA",
        "iso-char2": "IT",
    },

    {
        "worldbase-code": "365",
        "worldbase-char": "JM",
        "country-name": "Jamaica",
        "iso-digit": "388",
        "iso-char": "JAM",
        "iso-char2": "JM",
    },

    {
        "worldbase-code": "377",
        "worldbase-char": "JO",
        "country-name": "Jordan",
        "iso-digit": "400",
        "iso-char": "JOR",
        "iso-char2": "JO",
    },

    {
        "worldbase-code": "369",
        "worldbase-char": "JA",
        "country-name": "Japan",
        "iso-digit": "392",
        "iso-char": "JPN",
        "iso-char2": "JP",
    },

    {
        "worldbase-code": "925",
        "worldbase-char": "KZ",
        "country-name": "Kazakstan",
        "iso-digit": "398",
        "iso-char": "KAZ",
        "iso-char2": "KZ",
    },

    {
        "worldbase-code": "381",
        "worldbase-char": "KE",
        "country-name": "Kenya",
        "iso-digit": "404",
        "iso-char": "KEN",
        "iso-char2": "KE",
    },

    {
        "worldbase-code": "930",
        "worldbase-char": "XZ",
        "country-name": "Kyrgyzstan",
        "iso-digit": "417",
        "iso-char": "KGZ",
        "iso-char2": "KG",
    },

    {
        "worldbase-code": "379",
        "worldbase-char": "KA",
        "country-name": "Cambodia",
        "iso-digit": "116",
        "iso-char": "KHM",
        "iso-char2": "KH",
    },

    {
        "worldbase-code": "387",
        "worldbase-char": "KI",
        "country-name": "Kiribati",
        "iso-digit": "296",
        "iso-char": "KIR",
        "iso-char2": "KI",
    },

    {
        "worldbase-code": "629",
        "worldbase-char": "SJ",
        "country-name": "Saint Kitts & Nevis",
        "iso-digit": "659",
        "iso-char": "KNA",
        "iso-char2": "KN",
    },

    {
        "worldbase-code": "393",
        "worldbase-char": "KR",
        "country-name": "Korea, Republic of",
        "iso-digit": "410",
        "iso-char": "KOR",
        "iso-char2": "KR",
    },

    {
        "worldbase-code": "397",
        "worldbase-char": "KU",
        "country-name": "Kuwait",
        "iso-digit": "414",
        "iso-char": "KWT",
        "iso-char2": "KW",
    },

    {
        "worldbase-code": "401",
        "worldbase-char": "LA",
        "country-name": "Lao, People's Democratic Republic",
        "iso-digit": "418",
        "iso-char": "LAO",
        "iso-char2": "LA",
    },

    {
        "worldbase-code": "405",
        "worldbase-char": "LE",
        "country-name": "Lebanon",
        "iso-digit": "422",
        "iso-char": "LBN",
        "iso-char2": "LB",
    },

    {
        "worldbase-code": "413",
        "worldbase-char": "LB",
        "country-name": "Liberia",
        "iso-digit": "430",
        "iso-char": "LBR",
        "iso-char2": "LR",
    },

    {
        "worldbase-code": "417",
        "worldbase-char": "LI",
        "country-name": "Libyan Arab Jamahiriya",
        "iso-digit": "434",
        "iso-char": "LBY",
        "iso-char2": "LY",
    },

    {
        "worldbase-code": "633",
        "worldbase-char": "SQ",
        "country-name": "Saint Lucia",
        "iso-digit": "662",
        "iso-char": "LCA",
        "iso-char2": "LC",
    },

    {
        "worldbase-code": "421",
        "worldbase-char": "FL",
        "country-name": "Liechtenstein",
        "iso-digit": "438",
        "iso-char": "LIE",
        "iso-char2": "LI",
    },

    {
        "worldbase-code": "701",
        "worldbase-char": "SR",
        "country-name": "Sri Lanka",
        "iso-digit": "144",
        "iso-char": "LKA",
        "iso-char2": "LK",
    },

    {
        "worldbase-code": "409",
        "worldbase-char": "LS",
        "country-name": "Lesotho",
        "iso-digit": "426",
        "iso-char": "LSO",
        "iso-char2": "LS",
    },

    {
        "worldbase-code": "425",
        "worldbase-char": "LT",
        "country-name": "Lithuania",
        "iso-digit": "440",
        "iso-char": "LTU",
        "iso-char2": "LT",
    },

    {
        "worldbase-code": "429",
        "worldbase-char": "LX",
        "country-name": "Luxembourg",
        "iso-digit": "442",
        "iso-char": "LUX",
        "iso-char2": "LU",
    },

    {
        "worldbase-code": "935",
        "worldbase-char": "LV",
        "country-name": "Latvia",
        "iso-digit": "428",
        "iso-char": "LVA",
        "iso-char2": "LV",
    },

    {
        "worldbase-code": "433",
        "worldbase-char": "MA",
        "country-name": "Macau",
        "iso-digit": "446",
        "iso-char": "MAC",
        "iso-char2": "MO",
    },

    {
        "worldbase-code": "505",
        "worldbase-char": "MO",
        "country-name": "Morocco",
        "iso-digit": "504",
        "iso-char": "MAR",
        "iso-char2": "MA",
    },

    {
        "worldbase-code": "497",
        "worldbase-char": "MC",
        "country-name": "Monaco",
        "iso-digit": "492",
        "iso-char": "MCO",
        "iso-char2": "MC",
    },

    {
        "worldbase-code": "940",
        "worldbase-char": "MD",
        "country-name": "Moldova, Republic of",
        "iso-digit": "498",
        "iso-char": "MDA",
        "iso-char2": "MD",
    },

    {
        "worldbase-code": "441",
        "worldbase-char": "MG",
        "country-name": "Madagascar",
        "iso-digit": "450",
        "iso-char": "MDG",
        "iso-char2": "MG",
    },

    {
        "worldbase-code": "453",
        "worldbase-char": "MV",
        "country-name": "Maldives",
        "iso-digit": "462",
        "iso-char": "MDV",
        "iso-char2": "MV",
    },

    {
        "worldbase-code": "489",
        "worldbase-char": "MX",
        "country-name": "Mexico",
        "iso-digit": "484",
        "iso-char": "MEX",
        "iso-char2": "MX",
    },

    {
        "worldbase-code": "469",
        "worldbase-char": "MI",
        "country-name": "Marshall Islands",
        "iso-digit": "584",
        "iso-char": "MHL",
        "iso-char2": "MH",
    },

    {
        "worldbase-code": "965",
        "worldbase-char": "YR",
        "country-name": "Macedonia, The Former Yugoslav Republic Of",
        "iso-digit": "807",
        "iso-char": "MKD",
        "iso-char2": "MK",
    },

    {
        "worldbase-code": "457",
        "worldbase-char": "ML",
        "country-name": "Mali",
        "iso-digit": "466",
        "iso-char": "MLI",
        "iso-char2": "ML",
    },

    {
        "worldbase-code": "461",
        "worldbase-char": "MT",
        "country-name": "Malta",
        "iso-digit": "470",
        "iso-char": "MLT",
        "iso-char2": "MT",
    },

    {
        "worldbase-code": "510",
        "worldbase-char": "BM",
        "country-name": "Myanmar",
        "iso-digit": "104",
        "iso-char": "MMR",
        "iso-char2": "MM",
    },

    {
        "worldbase-code": "000",
        "worldbase-char": "000",
        "country-name": "Mongolia",
        "iso-digit": "496",
        "iso-char": "MNG",
        "iso-char2": "MN",
    },

    {
        "worldbase-code": "551",
        "worldbase-char": "MN",
        "country-name": "Northern Mariana Islands",
        "iso-digit": "580",
        "iso-char": "MNP",
        "iso-char2": "MP",
    },

    {
        "worldbase-code": "509",
        "worldbase-char": "MZ",
        "country-name": "Mozambique",
        "iso-digit": "508",
        "iso-char": "MOZ",
        "iso-char2": "MZ",
    },

    {
        "worldbase-code": "477",
        "worldbase-char": "MY",
        "country-name": "Mauritania",
        "iso-digit": "478",
        "iso-char": "MRT",
        "iso-char2": "MR",
    },

    {
        "worldbase-code": "501",
        "worldbase-char": "ME",
        "country-name": "Montserrat",
        "iso-digit": "500",
        "iso-char": "MSR",
        "iso-char2": "MS",
    },

    {
        "worldbase-code": "473",
        "worldbase-char": "MQ",
        "country-name": "Martinique",
        "iso-digit": "474",
        "iso-char": "MTQ",
        "iso-char2": "MQ",
    },

    {
        "worldbase-code": "481",
        "worldbase-char": "MU",
        "country-name": "Mauritius",
        "iso-digit": "480",
        "iso-char": "MUS",
        "iso-char2": "MU",
    },

    {
        "worldbase-code": "445",
        "worldbase-char": "MW",
        "country-name": "Malawi",
        "iso-digit": "454",
        "iso-char": "MWI",
        "iso-char2": "MW",
    },

    {
        "worldbase-code": "449",
        "worldbase-char": "MS",
        "country-name": "Malaysia",
        "iso-digit": "458",
        "iso-char": "MYS",
        "iso-char2": "MY",
    },

    {
        "worldbase-code": "937",
        "worldbase-char": "XM",
        "country-name": "Mayotte",
        "iso-digit": "175",
        "iso-char": "MYT",
        "iso-char2": "YT",
    },

    {
        "worldbase-code": "511",
        "worldbase-char": "NM",
        "country-name": "Namibia",
        "iso-digit": "516",
        "iso-char": "NAM",
        "iso-char2": "NA",
    },

    {
        "worldbase-code": "529",
        "worldbase-char": "NC",
        "country-name": "New Caledonia",
        "iso-digit": "540",
        "iso-char": "NCL",
        "iso-char2": "NC",
    },

    {
        "worldbase-code": "545",
        "worldbase-char": "NG",
        "country-name": "Niger",
        "iso-digit": "562",
        "iso-char": "NER",
        "iso-char2": "NE",
    },

    {
        "worldbase-code": "552",
        "worldbase-char": "NN",
        "country-name": "Norfolk Island",
        "iso-digit": "574",
        "iso-char": "NFK",
        "iso-char2": "NF",
    },

    {
        "worldbase-code": "549",
        "worldbase-char": "NI",
        "country-name": "Nigeria",
        "iso-digit": "566",
        "iso-char": "NGA",
        "iso-char2": "NG",
    },

    {
        "worldbase-code": "541",
        "worldbase-char": "NR",
        "country-name": "Nicaragua",
        "iso-digit": "558",
        "iso-char": "NIC",
        "iso-char2": "NI",
    },

    {
        "worldbase-code": "000",
        "worldbase-char": "000",
        "country-name": "Niue",
        "iso-digit": "570",
        "iso-char": "NIU",
        "iso-char2": "NU",
    },

    {
        "worldbase-code": "521",
        "worldbase-char": "NL",
        "country-name": "Netherlands",
        "iso-digit": "528",
        "iso-char": "NLD",
        "iso-char2": "NL",
    },

    {
        "worldbase-code": "553",
        "worldbase-char": "NO",
        "country-name": "Norway",
        "iso-digit": "578",
        "iso-char": "NOR",
        "iso-char2": "NO",
    },

    {
        "worldbase-code": "517",
        "worldbase-char": "NE",
        "country-name": "Nepal",
        "iso-digit": "524",
        "iso-char": "NPL",
        "iso-char2": "NP",
    },

    {
        "worldbase-code": "513",
        "worldbase-char": "NU",
        "country-name": "Nauru",
        "iso-digit": "520",
        "iso-char": "NRU",
        "iso-char2": "NR",
    },

    {
        "worldbase-code": "537",
        "worldbase-char": "NZ",
        "country-name": "New Zealand",
        "iso-digit": "554",
        "iso-char": "NZL",
        "iso-char2": "NZ",
    },

    {
        "worldbase-code": "561",
        "worldbase-char": "OM",
        "country-name": "Oman",
        "iso-digit": "512",
        "iso-char": "OMN",
        "iso-char2": "OM",
    },

    {
        "worldbase-code": "565",
        "worldbase-char": "PA",
        "country-name": "Pakistan",
        "iso-digit": "586",
        "iso-char": "PAK",
        "iso-char2": "PK",
    },

    {
        "worldbase-code": "569",
        "worldbase-char": "PN",
        "country-name": "Panama",
        "iso-digit": "591",
        "iso-char": "PAN",
        "iso-char2": "PA",
    },

    {
        "worldbase-code": "000",
        "worldbase-char": "000",
        "country-name": "Pitcairn",
        "iso-digit": "612",
        "iso-char": "PCN",
        "iso-char2": "PN",
    },

    {
        "worldbase-code": "585",
        "worldbase-char": "PR",
        "country-name": "Peru",
        "iso-digit": "604",
        "iso-char": "PER",
        "iso-char2": "PE",
    },

    {
        "worldbase-code": "589",
        "worldbase-char": "PH",
        "country-name": "Philippines",
        "iso-digit": "608",
        "iso-char": "PHL",
        "iso-char2": "PH",
    },

    {
        "worldbase-code": "000",
        "worldbase-char": "000",
        "country-name": "Palau",
        "iso-digit": "585",
        "iso-char": "PLW",
        "iso-char2": "PW",
    },

    {
        "worldbase-code": "901",
        "worldbase-char": "AY",
        "country-name": "Papua New Guinea",
        "iso-digit": "598",
        "iso-char": "PNG",
        "iso-char2": "PG",
    },

    {
        "worldbase-code": "573",
        "worldbase-char": "PP",
        "country-name": "Papua New Guinea",
        "iso-digit": "598",
        "iso-char": "PNG",
        "iso-char2": "PG",
    },

    {
        "worldbase-code": "597",
        "worldbase-char": "PL",
        "country-name": "Poland",
        "iso-digit": "616",
        "iso-char": "POL",
        "iso-char2": "PL",
    },

    {
        "worldbase-code": "805",
        "worldbase-char": "US",
        "country-name": "Puerto Rico",
        "iso-digit": "630",
        "iso-char": "PRI",
        "iso-char2": "PR",
    },

    {
        "worldbase-code": "389",
        "worldbase-char": "KD",
        "country-name": "Korea, Democratic People's Republic of",
        "iso-digit": "408",
        "iso-char": "PRK",
        "iso-char2": "KP",
    },

    {
        "worldbase-code": "601",
        "worldbase-char": "PO",
        "country-name": "Portugal",
        "iso-digit": "620",
        "iso-char": "PRT",
        "iso-char2": "PT",
    },

    {
        "worldbase-code": "581",
        "worldbase-char": "PG",
        "country-name": "Paraguay",
        "iso-digit": "600",
        "iso-char": "PRY",
        "iso-char2": "PY",
    },

    {
        "worldbase-code": "249",
        "worldbase-char": "FP",
        "country-name": "French Polynesia",
        "iso-digit": "258",
        "iso-char": "PYF",
        "iso-char2": "PF",
    },

    {
        "worldbase-code": "613",
        "worldbase-char": "QA",
        "country-name": "Qatar",
        "iso-digit": "634",
        "iso-char": "QAT",
        "iso-char2": "QA",
    },

    {
        "worldbase-code": "617",
        "worldbase-char": "RE",
        "country-name": "Reunion",
        "iso-digit": "638",
        "iso-char": "REU",
        "iso-char2": "RE",
    },

    {
        "worldbase-code": "620",
        "worldbase-char": "RO",
        "country-name": "Romania",
        "iso-digit": "642",
        "iso-char": "ROU",
        "iso-char2": "RO",
    },

    {
        "worldbase-code": "622",
        "worldbase-char": "RF",
        "country-name": "Russia Federation",
        "iso-digit": "643",
        "iso-char": "RUS",
        "iso-char2": "RU",
    },

    {
        "worldbase-code": "623",
        "worldbase-char": "RW",
        "country-name": "Rwanda",
        "iso-digit": "646",
        "iso-char": "RWA",
        "iso-char2": "RW",
    },

    {
        "worldbase-code": "657",
        "worldbase-char": "SD",
        "country-name": "Saudi Arabia",
        "iso-digit": "682",
        "iso-char": "SAU",
        "iso-char2": "SA",
    },

    {
        "worldbase-code": "705",
        "worldbase-char": "SU",
        "country-name": "Sudan",
        "iso-digit": "736",
        "iso-char": "SDN",
        "iso-char2": "SD",
    },

    {
        "worldbase-code": "661",
        "worldbase-char": "SG",
        "country-name": "Senegal",
        "iso-digit": "686",
        "iso-char": "SEN",
        "iso-char2": "SN",
    },

    {
        "worldbase-code": "677",
        "worldbase-char": "SI",
        "country-name": "Singapore",
        "iso-digit": "702",
        "iso-char": "SGP",
        "iso-char2": "SG",
    },

    {
        "worldbase-code": "947",
        "worldbase-char": "DW",
        "country-name": "South Georgia & The South Sandwich Islands",
        "iso-digit": "239",
        "iso-char": "SGS",
        "iso-char2": "GS",
    },

    {
        "worldbase-code": "944",
        "worldbase-char": "ZS",
        "country-name": "South Georgia & The South Sandwich Islands",
        "iso-digit": "239",
        "iso-char": "SGS",
        "iso-char2": "GS",
    },

    {
        "worldbase-code": "000",
        "worldbase-char": "000",
        "country-name": "South Georgia & The South Sandwich Islands",
        "iso-digit": "239",
        "iso-char": "SGS",
        "iso-char2": "GS",
    },

    {
        "worldbase-code": "035",
        "worldbase-char": "AI",
        "country-name": "Saint Helena",
        "iso-digit": "654",
        "iso-char": "SHN",
        "iso-char2": "SH",
    },

    {
        "worldbase-code": "626",
        "worldbase-char": "SH",
        "country-name": "Saint Helena",
        "iso-digit": "654",
        "iso-char": "SHN",
        "iso-char2": "SH",
    },

    {
        "worldbase-code": "000",
        "worldbase-char": "000",
        "country-name": "Svalbard and Jan Mayen",
        "iso-digit": "744",
        "iso-char": "SJM",
        "iso-char2": "SJ",
    },

    {
        "worldbase-code": "679",
        "worldbase-char": "SS",
        "country-name": "Solomon Islands",
        "iso-digit": "090",
        "iso-char": "SLB",
        "iso-char2": "SB",
    },

    {
        "worldbase-code": "669",
        "worldbase-char": "SL",
        "country-name": "Sierra Leone",
        "iso-digit": "694",
        "iso-char": "SLE",
        "iso-char2": "SL",
    },

    {
        "worldbase-code": "213",
        "worldbase-char": "EL",
        "country-name": "El Salvador",
        "iso-digit": "222",
        "iso-char": "SLV",
        "iso-char2": "SV",
    },

    {
        "worldbase-code": "649",
        "worldbase-char": "SM",
        "country-name": "San Marino",
        "iso-digit": "674",
        "iso-char": "SMR",
        "iso-char2": "SM",
    },

    {
        "worldbase-code": "681",
        "worldbase-char": "SO",
        "country-name": "Somalia",
        "iso-digit": "706",
        "iso-char": "SOM",
        "iso-char2": "SO",
    },

    {
        "worldbase-code": "635",
        "worldbase-char": "PM",
        "country-name": "Saint Pierre and Miquelon",
        "iso-digit": "666",
        "iso-char": "SPM",
        "iso-char2": "PM",
    },

    {
        "worldbase-code": "653",
        "worldbase-char": "ST",
        "country-name": "Sao Tome and Principe",
        "iso-digit": "678",
        "iso-char": "STP",
        "iso-char2": "ST",
    },

    {
        "worldbase-code": "709",
        "worldbase-char": "SN",
        "country-name": "Suriname",
        "iso-digit": "740",
        "iso-char": "SUR",
        "iso-char2": "SR",
    },

    {
        "worldbase-code": "680",
        "worldbase-char": "SK",
        "country-name": "Slovakia",
        "iso-digit": "703",
        "iso-char": "SVK",
        "iso-char2": "SK",
    },

    {
        "worldbase-code": "678",
        "worldbase-char": "SB",
        "country-name": "Slovenia",
        "iso-digit": "705",
        "iso-char": "SVN",
        "iso-char2": "SI",
    },

    {
        "worldbase-code": "717",
        "worldbase-char": "SW",
        "country-name": "Sweden",
        "iso-digit": "752",
        "iso-char": "SWE",
        "iso-char2": "SE",
    },

    {
        "worldbase-code": "713",
        "worldbase-char": "KS",
        "country-name": "Swaziland",
        "iso-digit": "748",
        "iso-char": "SWZ",
        "iso-char2": "SZ",
    },

    {
        "worldbase-code": "665",
        "worldbase-char": "SE",
        "country-name": "Seychelles",
        "iso-digit": "690",
        "iso-char": "SYC",
        "iso-char2": "SC",
    },

    {
        "worldbase-code": "725",
        "worldbase-char": "SY",
        "country-name": "Syrian Arab Republic",
        "iso-digit": "760",
        "iso-char": "SYR",
        "iso-char2": "SY",
    },

    {
        "worldbase-code": "765",
        "worldbase-char": "TC",
        "country-name": "Turks and Caicos Islands",
        "iso-digit": "796",
        "iso-char": "TCA",
        "iso-char2": "TC",
    },

    {
        "worldbase-code": "149",
        "worldbase-char": "CG",
        "country-name": "Chad",
        "iso-digit": "148",
        "iso-char": "TCD",
        "iso-char2": "TD",
    },

    {
        "worldbase-code": "741",
        "worldbase-char": "TG",
        "country-name": "Togo",
        "iso-digit": "768",
        "iso-char": "TGO",
        "iso-char2": "TG",
    },

    {
        "worldbase-code": "733",
        "worldbase-char": "TH",
        "country-name": "Thailand",
        "iso-digit": "764",
        "iso-char": "THA",
        "iso-char2": "TH",
    },

    {
        "worldbase-code": "945",
        "worldbase-char": "TJ",
        "country-name": "Tajikistan",
        "iso-digit": "762",
        "iso-char": "TJK",
        "iso-char2": "TJ",
    },

    {
        "worldbase-code": "946",
        "worldbase-char": "ZT",
        "country-name": "Tokelau",
        "iso-digit": "772",
        "iso-char": "TKL",
        "iso-char2": "TK",
    },

    {
        "worldbase-code": "950",
        "worldbase-char": "TM",
        "country-name": "Turkmenistan",
        "iso-digit": "795",
        "iso-char": "TKM",
        "iso-char2": "TM",
    },

    {
        "worldbase-code": "000",
        "worldbase-char": "000",
        "country-name": "East Timor",
        "iso-digit": "626",
        "iso-char": "TMP",
        "iso-char2": "TP",
    },

    {
        "worldbase-code": "745",
        "worldbase-char": "TO",
        "country-name": "Tonga",
        "iso-digit": "776",
        "iso-char": "TON",
        "iso-char2": "TO",
    },

    {
        "worldbase-code": "749",
        "worldbase-char": "TT",
        "country-name": "Trinidad and Tobago",
        "iso-digit": "780",
        "iso-char": "TTO",
        "iso-char2": "TT",
    },

    {
        "worldbase-code": "757",
        "worldbase-char": "TU",
        "country-name": "Tunisia",
        "iso-digit": "788",
        "iso-char": "TUN",
        "iso-char2": "TN",
    },

    {
        "worldbase-code": "761",
        "worldbase-char": "TK",
        "country-name": "Turkey",
        "iso-digit": "792",
        "iso-char": "TUR",
        "iso-char2": "TR",
    },

    {
        "worldbase-code": "767",
        "worldbase-char": "TV",
        "country-name": "Tuvalu",
        "iso-digit": "798",
        "iso-char": "TUV",
        "iso-char2": "TV",
    },

    {
        "worldbase-code": "161",
        "worldbase-char": "CT",
        "country-name": "Taiwan, Province of China",
        "iso-digit": "158",
        "iso-char": "TWN",
        "iso-char2": "TW",
    },

    {
        "worldbase-code": "729",
        "worldbase-char": "TA",
        "country-name": "Tanzania, United Republic of",
        "iso-digit": "834",
        "iso-char": "TZA",
        "iso-char2": "TZ",
    },

    {
        "worldbase-code": "769",
        "worldbase-char": "UG",
        "country-name": "Uganda",
        "iso-digit": "800",
        "iso-char": "UGA",
        "iso-char2": "UG",
    },

    {
        "worldbase-code": "771",
        "worldbase-char": "UI",
        "country-name": "Ukraine",
        "iso-digit": "804",
        "iso-char": "UKR",
        "iso-char2": "UA",
    },

    {
        "worldbase-code": "938",
        "worldbase-char": "IM",
        "country-name": "United States Minor Outlying Islands",
        "iso-digit": "581",
        "iso-char": "UMI",
        "iso-char2": "UM",
    },

    {
        "worldbase-code": "970",
        "worldbase-char": "WK",
        "country-name": "United States Minor Outlying Islands",
        "iso-digit": "581",
        "iso-char": "UMI",
        "iso-char2": "UM",
    },

    {
        "worldbase-code": "000",
        "worldbase-char": "000",
        "country-name": "United States Minor Outlying Islands",
        "iso-digit": "581",
        "iso-char": "UMI",
        "iso-char2": "UM",
    },

    {
        "worldbase-code": "813",
        "worldbase-char": "UR",
        "country-name": "Uruguay",
        "iso-digit": "858",
        "iso-char": "URY",
        "iso-char2": "UY",
    },

    {
        "worldbase-code": "805",
        "worldbase-char": "US",
        "country-name": "United States",
        "iso-digit": "840",
        "iso-char": "USA",
        "iso-char2": "US",
    },

    {
        "worldbase-code": "955",
        "worldbase-char": "UZ",
        "country-name": "Uzbekistan",
        "iso-digit": "860",
        "iso-char": "UZB",
        "iso-char2": "UZ",
    },

    {
        "worldbase-code": "819",
        "worldbase-char": "VT",
        "country-name": "Holy See (Vatican City State)",
        "iso-digit": "336",
        "iso-char": "VAT",
        "iso-char2": "VA",
    },

    {
        "worldbase-code": "637",
        "worldbase-char": "SV",
        "country-name": "Saint Vincent and the Grenadines",
        "iso-digit": "670",
        "iso-char": "VCT",
        "iso-char2": "VC",
    },

    {
        "worldbase-code": "821",
        "worldbase-char": "VE",
        "country-name": "Venezuela",
        "iso-digit": "862",
        "iso-char": "VEN",
        "iso-char2": "VE",
    },

    {
        "worldbase-code": "093",
        "worldbase-char": "BV",
        "country-name": "Virgin Islands, British",
        "iso-digit": "092",
        "iso-char": "VGB",
        "iso-char2": "VG",
    },

    {
        "worldbase-code": "805",
        "worldbase-char": "US",
        "country-name": "Virgin Islands, U.S.",
        "iso-digit": "850",
        "iso-char": "VIR",
        "iso-char2": "VI",
    },

    {
        "worldbase-code": "829",
        "worldbase-char": "VI",
        "country-name": "Vietnam",
        "iso-digit": "704",
        "iso-char": "VNM",
        "iso-char2": "VN",
    },

    {
        "worldbase-code": "816",
        "worldbase-char": "VA",
        "country-name": "Vanuatu",
        "iso-digit": "548",
        "iso-char": "VUT",
        "iso-char2": "VU",
    },

    {
        "worldbase-code": "841",
        "worldbase-char": "WF",
        "country-name": "Wallis and Futuna",
        "iso-digit": "876",
        "iso-char": "WLF",
        "iso-char2": "WF",
    },

    {
        "worldbase-code": "641",
        "worldbase-char": "WS",
        "country-name": "Samoa",
        "iso-digit": "882",
        "iso-char": "WSM",
        "iso-char2": "WS",
    },

    {
        "worldbase-code": "853",
        "worldbase-char": "YE",
        "country-name": "Yemen",
        "iso-digit": "887",
        "iso-char": "YEM",
        "iso-char2": "YE",
    },

    {
        "worldbase-code": "857",
        "worldbase-char": "YM",
        "country-name": "Yemen",
        "iso-digit": "887",
        "iso-char": "YEM",
        "iso-char2": "YE",
    },

    {
        "worldbase-code": "861",
        "worldbase-char": "YU",
        "country-name": "Yugoslavia",
        "iso-digit": "891",
        "iso-char": "YUG",
        "iso-char2": "YU",
    },

    {
        "worldbase-code": "685",
        "worldbase-char": "SA",
        "country-name": "South Africa",
        "iso-digit": "710",
        "iso-char": "ZAF",
        "iso-char2": "ZA",
    },
]


def thread(rows, function):
    with ThreadPoolExecutor(max_workers=10) as executor:
        future_to_row = {executor.submit(
            function, index, row): row for index, row in enumerate(rows)}

        for future in as_completed(future_to_row):
            try:
                future.result()
            except Exception as e:
                print(e)


def to_text(text):
    if (isinstance(text, int) or (isinstance(text, float)) and text.is_integer()):
        return str(int(text))

    if text:
        text = re.sub(r'[^\x20-\x7E]+', '', str(text))
        text = re.sub(r'\s+', ' ', text)
        return text.strip()
    else:
        return ""


def to_float(value):
    if value:
        try:
            value = round(float(to_text(value)), 2)
        except:
            value = 0
    else:
        value = 0

    if value == int(value):
        return int(value)
    else:
        return value


def to_int(value):
    return int(to_float(value))


def to_date(value):
    try:
        date = datetime.strptime(
            str(value), "%m/%d/%Y").date() if value else None
        return date
    except:
        return None


def to_handle(text):
    if text:
        handle = str(text).lower().replace(" ", "-")
        handle = re.sub(r'[^a-z0-9-]', '', handle)
        handle = re.sub(r'-+', '-', handle)

        return handle.strip('-')
    else:
        return ""


def to_country(code):
    for country in COUNTRY_DICT:
        if code == country['worldbase-code'] or code == country['iso-digit']:
            return country['iso-char2']

    return "US"


def to_phone(country, phone_number):
    try:
        parsed_number = phonenumbers.parse(phone_number, country)
        formatted_number = phonenumbers.format_number(
            parsed_number, PhoneNumberFormat.INTERNATIONAL)
        return formatted_number
    except phonenumbers.phonenumberutil.NumberParseException:
        return None
