import requests, re, os
from bs4 import BeautifulSoup

#enter your course codes as shown below
module_list = ['ST2217', 'MK2100', 'MG2100', 'EC2100', 'AY207', 'FA2206']
download_folder = os.getcwd()

def download_pdfs(module, urls):

    os.chdir(download_folder + '\\' + module)
    semester_map = {'1': 'sem-1', '2': 'sem-2', '3':'autumn'}
    for file_url in urls:
      
        r = requests.get(file_url, stream = True) 
        divs = re.split("[& =]+", file_url)
        year = divs[divs.index('academic_session')+1]
        paper = divs[divs.index('paper_code_nominal')+1]
        try:
            semester = semester_map[divs[divs.index('assessment_period')+1]]
        except:
            semester = 'XX' + divs[divs.index('assessment_period')+1]
        
        name = year + '-' + paper + '-' + semester + '.pdf'
        
        with open(name,"wb") as pdf: 
            for chunk in r.iter_content(chunk_size=1024): 
                 if chunk: 
                     pdf.write(chunk)

def find_pdfs(module):

    url_start = "https://www.mis.nuigalway.ie/regexam/paper_index_help.asp?name=results_pane"
    r = requests.get(url_start)
    
    headers = {'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) ' + 'AppleWebKit/537.36 (KHTML, like Gecko) ' + 'Chrome/71.0.3578.98 Safari/537.37',
               'Host': 'www.mis.nuigalway.ie',
               'Referrer': 'ttps://www.mis.nuigalway.ie/regexam/paper_index_search_main_menu.asp',
               'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
               'Accept-Encoding': 'gzip, deflate, br',
               'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',
               'Cache-Control': 'no-cache',
               'Connection': 'keep-alive',
               'Pragma': 'no-cache',
               'Upgrade-Insecure-Requests': '1'}
    
    cookie = {'Cookie': r.headers['Set-Cookie']}
    headers.update(cookie)
    
    url_results = 'https://www.mis.nuigalway.ie/regexam/paper_index_search_results.asp'
    data = {"module": module}

    r = requests.post(url_results, headers=headers, data=data)
    
    soup = BeautifulSoup(r.content, "html.parser")
        
    links = []
    for tag in soup.findAll('a'):
            link = tag.get('href')
            if link is not None and 'download' in link:
                links.append('https://www.mis.nuigalway.ie/regexam/' + link)

    download_pdfs(module, links)



if __name__ == '__main__':
    
    for module in module_list:
        
        os.chdir(download_folder)
        os.makedirs(module)
        find_pdfs(module)