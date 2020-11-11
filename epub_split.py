template = """<?xml version='1.0' encoding='utf-8'?>
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
    <title>{skazka_name}</title>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
    <link rel="stylesheet" type="text/css" href="stylesheet.css"/>
    <link rel="stylesheet" type="text/css" href="page_styles.css"/>
</head>
<body>
    {narod}<h2 id="calibre_pb_{skazka_num}">{skazka_name}</h2>
</body>
{skazka_data}
</html>
"""
if __name__ == '__main__':
    with open('C:/Users/Наташа/Downloads/tmp.htm', 'r', encoding='utf-8-sig') as f:
        raw_data = f.read()
    skazka_num = 0
    for narod in [i for i in raw_data.split('<h1>') if i]:
        first_in_narod = True
        narod_name, narod_data = narod.split('</h1>', 1)
        print(narod_name)
        for skazka in [i for i in narod_data.split('<h2>') if i.strip()]:
            skazka_name, skazka_data = skazka.split('</h2>', 1)
            print('-', skazka_name)
            # write
            with open('C:/Users/Наташа/Downloads/1/proiekt_split_{}.htm'.format(str(skazka_num+1).zfill(3)), 'w',
                      encoding='utf-8') as f:
                f.write(template.format(
                    skazka_name=skazka_name,
                    narod='<h1>{}</h1>\n    '.format(narod_name) if first_in_narod else '',
                    skazka_num=str(skazka_num).zfill(2),
                    skazka_data=skazka_data,
                ))
            first_in_narod = False
            skazka_num += 1

