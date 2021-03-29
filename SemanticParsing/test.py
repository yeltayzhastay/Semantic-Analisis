import Vk_parser as parser

# 'https://oauth.vk.com/authorize?client_id=7651557&display=page&redirect_uri=https://oauth.vk.com/blank.html&scope=friends,groups&response_type=token&v=5.65'

token = "7ba6938f287fc7c5f623b1daf747dc9307ad66a076d4208b5e41216238869ade524fab1fc06cd8cdc3557"

vk_parse = parser.Vk_parser(token)
print(vk_parse.SearchGroup('преступление'))