HTML_0 = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <title>Theses | Boğaziçi University Perceptual Intelligence Lab</title>
    <meta content="width=device-width, initial-scale=1.0" name="viewport">

    <link href="static/css/bootstrap.css" rel="stylesheet">
    <link href="static/css/flat-ui.css" rel="stylesheet">
    <link href="static/css/lab.css" rel="stylesheet">

    <link href="images/favicon.ico" rel="shortcut icon">

    <!-- HTML5 shim, for IE6-8 support of HTML5 elements. All other JS at the end of file. -->
    <!--[if lt IE 9]>
    <script src="static/js/html5shiv.js"></script>
    <script src="static/js/respond.min.js"></script>
    <![endif]-->
</head>
<body data-spy="scroll" data-target="#affix-nav">
<nav class="navbar navbar-default navbar-fixed-top" role="navigation">
    <div class="container">
        <div class="navbar-header">
            <button class="navbar-toggle" data-target="#navbar-collapse" data-toggle="collapse" type="button">
                <span class="sr-only">Toggle navigation</span>
            </button>
            <a class="navbar-brand" href="/" title="Perceptual Intelligence Lab">PILAB</a>
        </div>

        <div class="collapse navbar-collapse" id="navbar-collapse">
            <ul class="nav navbar-nav">
                <li>
                    <a href="/">Home</a>
                </li>


                <li>
                    <a href="people.html">People</a>
                </li>


                <li>
                    <a href="projects.html">Projects</a>
                </li>


                <li>
                    <a href="publications.html">Publications</a>
                </li>


                <li class="active">
                    <a href="theses.html">Theses</a>
                </li>


                <li>
                    <a href="courses.html">Courses</a>
                </li>


                <li>
                    <a href="resources.html">Resources</a>
                </li>

            </ul>
            <ul class="nav navbar-nav navbar-right visible-lg">
                <li><a href="http://www.boun.edu.tr/" title="Boğaziçi University">BU</a></li>
                <li>
                    <a href="http://www.cmpe.boun.edu.tr/" title="Boğaziçi University Computer Engineering Department">
                        CmpE
                    </a>
                </li>
            </ul>
        </div>
    </div>
</nav>

<div class="container">
    <div class="row">
        <div class="col-md-10 col-md-offset-1">
"""

HTML_1 = """
        </div>
    </div>

    <footer>
        <hr>
        <p class="text-center">
            &copy;
            <a href="http://www.boun.edu.tr/">Boğaziçi University</a>
            <a href="http://www.cmpe.boun.edu.tr/">Computer Engineering Department</a>
            2020
        </p>
    </footer>
</div>

<script src="//ajax.googleapis.com/ajax/libs/jquery/2.0.3/jquery.min.js"></script>
<script>
    window.jQuery || document.write('<script src="static/js/jquery-2.0.3.min.js"><\/script>')
</script>
<script src="static/js/bootstrap.min.js"></script>

<script type="text/javascript">
    var _gaq = _gaq || [];
    _gaq.push(['_setAccount', 'UA-124225373-1']);
    _gaq.push(['_trackPageview']);

    (function () {
        var ga = document.createElement('script');
        ga.type = 'text/javascript';
        ga.async = true;
        ga.src = ('https:' == document.location.protocol ? 'https://ssl' : 'http://www') + '.google-analytics.com/ga.js';
        var s = document.getElementsByTagName('script')[0];
        s.parentNode.insertBefore(ga, s);
    })();
</script>
</body>
</html>
"""

def crawl_theses(URL):
    import requests
    from bs4 import BeautifulSoup

    COL = """
        <tr class="even">
                  <td class="views-field views-field-field-thesis-advisor">
            Lale Akarun          </td>
                  <td class="views-field views-field-title">
            <a href="https://www.cmpe.boun.edu.tr/content/real-time-human-hand-pose-estimation-and-tracking-using-depth-sensors">Real Time Human Hand Pose Estimation And Tracking Using Depth Sensors</a>          </td>
                  <td class="views-field views-field-field-thesis-type">
            <a href="https://www.cmpe.boun.edu.tr/thesis-type/phd" typeof="skos:Concept" property="rdfs:label skos:prefLabel">PhD</a>          </td>
                  <td class="views-field views-field-field-assigned-to">
            Mustafa Furkan Kirac          </td>
                  <td class="views-field views-field-field-thesis-year">
            <span class="date-display-single" property="dc:date" datatype="xsd:dateTime" content="2013-01-01T00:00:00+02:00">2013</span>          </td>
                  <td class="views-field views-field-field-co-advisor">
                      </td>
        </tr>
    """


    page = requests.get(URL)
    soup = BeautifulSoup(page.content, 'html.parser')
    theses = soup.find_all('tr')

    theses_content = []
    for thesis in theses[1:]:
        advisor = thesis.find('td', class_='views-field-field-thesis-advisor').text.strip()
        title = thesis.find('td', class_='views-field-title').text.strip()
        link = thesis.find('td', class_='views-field-title').a['href']
        type = thesis.find('td', class_='views-field-field-thesis-type').text.strip()
        author = thesis.find('td', class_='views-field-field-assigned-to').text.strip()
        year = thesis.find('td', class_='views-field-field-thesis-year').text.strip()
        co_advisor = thesis.find('td', class_='views-field-field-co-advisor').text.strip()

        theses_content.append({
            'advisor': advisor,
            'title': title,
            'link': link,
            'type': type,
            'author': author,
            'year': year,
            'co-advisor': co_advisor
        })

    return theses_content

def order_theses(theses):
    # first order by thesis type, then by year
    import pandas as pd
    thesis_df = pd.DataFrame(theses)
    thesis_df['year'] = thesis_df['year'].str.extract(r'(\d{4})')
    # filter absent years
    thesis_df = thesis_df[thesis_df['year'].notnull()]
    thesis_df['year'] = thesis_df['year'].astype(int)
    thesis_df = thesis_df.sort_values(by=['type', 'year'], ascending=[False, False])
    thesis_df['year'] = thesis_df['year'].astype(str)
    print(thesis_df.to_markdown())
    theses = thesis_df.to_dict(orient='records')
    return theses

def generate_thesis_html(theses):
    
    thesis_html = ''
    year = None
    thesis_type = None
    for thesis in theses:

        if thesis_type != thesis['type']:
            thesis_type = thesis['type']
            thesis_html += f"""
            <h1 class="lab-section-title">{thesis_type} Theses</h1>
            """
        
        if year != thesis['year']:
            year = thesis['year']
            thesis_html += f"""
            <div class="row-fluid">
                <h2 class="lab-subsection-title">{year}</h2>
            </div>
            """
        
        description = f"""by {thesis['author']} in {thesis['year']} under the supervision of {thesis['advisor']}"""
        if thesis['co-advisor']: description += f""" and co-advised by {thesis['co-advisor']}"""         

        thesis_html += f"""

            <div class="row">
                <div class="col-xs-12">
                    <div class="panel panel-default lab-panel">
                        <div class="panel-body">
                            <a href="https://www.cmpe.boun.edu.tr{thesis['link']}">
                                <div class="small-title">{thesis['title']}</div>
                            </a>
                            <div>{description}</div>
                        </div>
                    </div>
                </div>
            </div>

        """

    return thesis_html


def generate_thesis_page(thesis_html):
    with open('../theses.html', 'w') as f:
        f.write(HTML_0)
        f.write(thesis_html)
        f.write(HTML_1)


def main():
    URL = 'https://www.cmpe.boun.edu.tr/completed-theses?field_thesis_type_tid=All&field_thesis_advisor_value=Lale+Akarun'
    theses = crawl_theses(URL)

    URL = 'https://www.cmpe.boun.edu.tr/completed-theses?field_thesis_type_tid=All&field_thesis_advisor_value=Albert+Ali+Salah'
    theses += crawl_theses(URL)

    URL = 'https://www.cmpe.boun.edu.tr/completed-theses?field_thesis_type_tid=All&field_thesis_advisor_value=Fikret+G%C3%BCrgen'
    theses += crawl_theses(URL)

    theses = order_theses(theses)
    
    thesis_html = generate_thesis_html(theses)

    generate_thesis_page(thesis_html)

if __name__ == '__main__':
    main()