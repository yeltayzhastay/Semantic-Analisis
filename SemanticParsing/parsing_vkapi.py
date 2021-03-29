import Vk_parser as parser
import time

def main():
    first_time = time.time()

    access_token = "0a93bf3e5e613f7f8330cccc4df8fba77079c92d520a615a4cd7897ebb7d1808ad3e379a25ee58e681fbb"
    getter = parser.Vk_parser(access_token)
    ids = getter.SearchGroup('қылмыс')

    token = "2002bd1a2002bd1a2002bd1a5d20767dff220022002bd1a400ae31246fd06003f1a23d5"
    vk_parse = parser.Vk_parser(access_token)
    vk_parse.Get_sentimental(ids, 10)
    vk_parse.to_csv('dataset20_01_21kaz.csv')

    print('Parsing data finished!', round(time.time() - first_time, 2), 'sec')

if __name__ == "__main__":
    main()