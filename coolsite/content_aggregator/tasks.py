from __future__ import absolute_import, unicode_literals
from bs4 import BeautifulSoup
from celery import shared_task
from celery.utils.log import get_task_logger
from fake_useragent import UserAgent
from .models import Article, Category
import requests


logger = get_task_logger(__name__)

@shared_task(serializer='json')
def save_function(article_list): 
    for article in article_list:
        categories = [category.name.lower() for category in Category.objects.all()]
        try:
            if article['category'] in categories:
                category = Category.objects.get(name=article['category'].capitalize())
            else:
                category = Category.objects.create(name=article['category'].capitalize())
                print(f'[+] Добавлена новая категория - {category}')
                
            Article.objects.create(
                title = article['title'],
                content = article['content'],
                category = category,
                is_published = 1,
                source = article['source']
            )
            print(f'[+] Статья записана, категория - {category}')
        except Exception as e:
            print(e)
            break
    else:
        return print('finished')


@shared_task
def interfax_parser():
    ua = UserAgent()
    main_link = 'https://www.interfax.ru/'
    
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'User-Agent': ua.random
    }
    
    article_list = []
    try:
        print('Starting the scraping tool')
        response = requests.get(url=f'{main_link}news/', headers=headers)
        soup = BeautifulSoup(response.text, 'lxml')

        articles = soup.select('div[data-id]')
        
        for article in articles:
            link = article.find('a')
            title = link.find('h3').text.strip()
                   
            if link['href'][:5] == 'https':
                url = link['href']
            else:
                url = f"{main_link}{link['href']}"
            
            print(url)
            
            article_response = requests.get(url=url, headers=headers)
            article_response.encoding = 'cp1251'
            article_soup = BeautifulSoup(article_response.text, 'lxml')
            
            page_content = article_soup.find('div', class_='infinitblock')
            category = page_content.find('aside', class_='textML').find('a').text.lower().strip()
            
            content = page_content.find('article').find_all('p')
            result_content = []
            
            for paragraph in content:
                result_content.append(paragraph.text.strip())
            
            result_content = '\n\n'.join(result_content)
            article = {
                'title': title,
                'content': result_content,
                'category': category,
                'source': url
            }

            article_list.append(article)

        print('Finished scraping the articles')
            
    except Exception as e:
        print('The scraping job failed. See exception:')
        print(e)
        
    return(save_function(article_list))


@shared_task
def lenta_parser():
    ua = UserAgent()
    main_link = 'https://lenta.ru/'
    
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'User-Agent': ua.random
    }
    
    article_list = []
    try:
        print('Starting the scraping tool')
        response = requests.get(url=f'{main_link}parts/text/', headers=headers)
        soup = BeautifulSoup(response.text, 'lxml')

        articles = soup.find_all('li', class_='parts-page__item')
        for article in articles:
            link = article.find('a')
            title = link.find('div', class_='card-big__titles').find('h3').text.strip()
                   
            if link['href'][:5] == 'https':
                url = link['href']
            else:
                url = f"{main_link}{link['href']}"
            
            print(url)
            
            article_response = requests.get(url=url, headers=headers)
            article_soup = BeautifulSoup(article_response.text, 'lxml')
            
            page_content = article_soup.find('div', class_='topic-page__container')
            category = page_content.find('a', class_='topic-header__rubric').text.lower().strip()
            content = page_content.find('div', class_='topic-body__content').find_all('p')
            if content:
                result_content = []
                
                for paragraph in content:
                    p = paragraph.text.strip()
                    if 'фото' not in p.split(':'):
                        result_content.append(p)
                
                result_content = '\n\n'.join(result_content)
                article = {
                    'title': title,
                    'content': result_content,
                    'category': category,
                    'source': url
                }
            else:
                continue
            article_list.append(article)
        print('Finished scraping the articles')
            
    except Exception as e:
        print('The scraping job failed. See exception:')
        print(e)
        
    return save_function(article_list)

@shared_task
def autoru_parser():
    ua = UserAgent()
    main_link = 'https://mag.auto.ru/theme/news/'
    
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'User-Agent': ua.random
    }
    
    article_list = []
    try:
        print('Starting the scraping tool')
        response = requests.get(url=f'{main_link}', headers=headers)
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.text, 'lxml')

        articles = soup.find_all('article', class_='BlockTypePost')
        for article in articles:
            link = article.find('a')['href']
            title = article.find('h3', class_='BlockTypePost__title').find('a')
        
            if title:
                title = title.text.strip()
            
            article_response = requests.get(url=link, headers=headers)
            article_response.encoding = 'utf-8'
            article_soup = BeautifulSoup(article_response.text, 'lxml')
            
            page_content = article_soup.find('main')
            content = page_content.find('div', class_='MarkupText').find('p')
            if content:
                result_content = []
                
                for paragraph in content:
                    result_content.append(paragraph.text.strip())
                
                result_content = '\n\n'.join(result_content)
                article = {
                    'title': title,
                    'content': result_content,
                    'category': 'авто',
                    'source': link
                }
                article_list.append(article)
        print('Finished scraping the articles')
            
    except Exception as e:
        print('The scraping job failed. See exception:')
        print(e)
        
    return save_function(article_list)