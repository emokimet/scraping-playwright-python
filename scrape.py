import asyncio
import random
import csv, json, os, tempfile
from playwright.async_api import async_playwright, TimeoutError
from playwright_stealth import stealth_async
title=""
category = []
color = []
size = []
dir_name = ""
async def main():
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
        )
        page = await context.new_page()
        # Evaluate navigator.webdriver before applying stealth measures
        await page.context.clear_cookies()
        # Clear the storage state (including cache) for the current context
        await page.context.clear_permissions()
        before_stealth = await page.evaluate('''() => navigator.webdriver''')
        print("Before applying stealth measures: ", before_stealth)
        # Apply stealth measures
        await stealth_async(page)
        print("Loading page: https://www.buyma.com/login/...")
        await page.goto('https://www.buyma.com/login/', timeout=100000)
        after_stealth = await page.evaluate('''() => navigator.webdriver''')
        print("After applying stealth measures:", after_stealth)
        await fill_signin(page)
        

async def scrape_data(url, page):
    url = url
    await asyncio.sleep(random.uniform(10.0, 20.0))
    print("Loading page: "+ url+"...")
    await page.goto("https://www.buyma.com/item/107111530/", timeout=600000)
    print("scraping data...")
    title = await page.query_selector('//*[@id="item_h1"]/span')
    title = await title.text_content()
    print(title)
    """content = []
    
    content.append(title)
    price = await page.query_selector('//*[@id="abtest_display_pc"]')
    price = await price.text_content()
    content.append(price)"""
    category_elements = await page.query_selector_all('//*[@id="s_cate"]/dd/ul/li/a')
    for element in category_elements:
        category.append(await element.text_content())
    print(category)
    #print(category_elements)
    """for element in category_elements
    category_element = [sub_category.text_content() for sub_category in category_elements]
    category.append(category_element)"""
    await registration_list(page)
    
    #print(category)
    #content.append(category)

 
    """json_data = await page.query_selector('.js-sizes-with-colors')
    json_data = await json_data.text_content()
    data = json.loads(json_data)
    color_list = []
    size_list = []
    for item in data:
        colors = item.get('colors', [])
        for color in colors:
            color_name = color.get('color_name')
            if color_name in color_list:
                continue
            else:
                color_list.append(color_name)
        size_master_name = item.get("size_master_name")
        if size_master_name in size_list:
            continue
        else:
            size_list.append(size_master_name)
    print(color_list)
    content.append(color_list)
    content.append(size_list)
    print(content)
    print("-------")
    return content"""

async def fill_signin(page):

        await page.focus('//*[@id="txtLoginId"]')
        await page.fill('input[id="txtLoginId"]', 'riras58785@kinsef.com')
        await page.focus('input[id="txtLoginPass"]')
        await page.fill('input[id="txtLoginPass"]', '5IoZNM4xk3zR8x')
        print("Login...")
        await page.keyboard.press('Enter')
           # Call the function to process CSV data
        try:
            #await save_csv_text(page)
            await scrape_data('https://www.buyma.com/item/107111530/', page)
        except StopIteration:
            print("StopIteration exception encountered.")
        except Exception as e:
            print(f"An error occurred: {e}")

async def extract_text(page, selector):

    elements = await page.query_selector_all(selector)
    texts = []
    for element in elements:
        texts.append(await element.inner_text() if element else "")
    return texts

async def save_csv_text(page):
    # Read data from CSV file using csv.reader
    line_count = 0
    updated_rows = list()
    with open('e:/resume/scrap_python/scrapping.csv', mode='r', newline='', encoding="utf-8-sig") as csvfile:
        csv_reader = csv.reader(csvfile)
        result=[]
        updated_rows.clear()
        for row in csv_reader:
            if not row:
                break
            if line_count == 0:
                line_count += 1
                continue
            else:
                col1_value = row[0]  # Access the first column by index
                if col1_value:
                    result = await scrape_data(col1_value, page)
                    print(result)
                    result.insert(0, col1_value)
                    updated_rows.append(result)
            line_count += 1  
        csvfile.close() 

    # Write the updated rows back to the CSV file
    with open('e:/resume/scrap_python/scrapping.csv', mode='a', newline='', encoding="utf-8-sig") as csvfile_updated:
        employee_writer = csv.writer(csvfile_updated)
        print("Save file...")
        employee_writer.writerows(updated_rows)
        print("Successed")
        csvfile_updated.close()
print("Starting...") 

async def registration_list(page):
    print('Registering information...')

    await asyncio.sleep(random.uniform(10.0, 20.0))
    await page.goto('https://www.buyma.com/my/sell/new/?tab=b', timeout=100000)
    popup = await page.query_selector('button[class="driver-close-btn"]')
    await popup.click()
    await register_image(page)
    await register_title(page, title)
    await register_category(page, category)
    await register_color(page)
    input("----------")



    
async def register_title(page, title):
    print('Registering title...')

    title = title
    title_input = await page.query_selector("input[class='bmm-c-text-field']")
    print(type(title))
    await title_input.fill("オシャレ♪【LOUISVUITTON】タイムアウト・ライン スニーカー")

async def register_category(page, category):
    
    print('Registering category...')

    for item in category:
        category_list = await page.query_selector_all('.sell-category__item')
        index = category.index(item)
        print(index)
        category_select = category_list[index]
        await category_select.click()
        if item=='レディースファッション':
            print("ddddddddddddddd")
        print(item)
        category_1 = await page.wait_for_selector("div[aria-label='"+item+"']")
        print("---------")

        await category_1.click()
        print("---------")
    


async def register_color(page):
    print("Registering color...")
    """# Select color
    select_color = await page.query_selector(".sell-color-option")
    await select_color.click()"""
    list2 = [
        "ホワイト",
        "ブラック",
        "グレー",
        "ブラウン",
        "ベージュ",
        "グリーン",
        "ブルー",
        "ネイビー",
        "パープル",
        "イエロー",
        "ピンク",
        "レッド",
        "オレンジ",
        "シルバー",
        "ゴールド",
        "クリア",
        "マルチカラー"
    ]
    list1 = ['ホワイト※要在庫確認', 'ブラック※要在庫確認']
    for element1 in list1:

        for element2 in list2:
            if element2 in element1:
                print(f"Found common string: {element1}")
                # You can return the element or perform an action on it
                add_color = await page.query_selector_all("td>.bmm-c-custom-select")
                add_color = add_color[list1.index(element1)]
                await add_color.click()
                print(element2)
                select_color = await page.wait_for_selector("div[aria-label^='"+element2+"']")
                await select_color.click()
                add_color = await page.query_selector(".bmm-c-form-table__foot>a")
                await add_color.click()
                add_color.click()
    input("---------2")
    print("No common string found")

async def register_image(page):

# Upload image
    #folder_path = get_temp_dir()
    image = await page.query_selector('input[type="file"]')
    await image.evaluate("(element) => { element.style.display = 'block'; }")
    await image.set_input_files(await get_files_in_folder("E:/resume/product"))
    #print("Uploaded file from" + await get_files_in_folder('E:/resume/product'))

async def get_temp_dir():

    async with async_playwright() as p:
        temp_dir = tempfile.gettempdir()+"image_folder_buyma"
        return temp_dir
    
async def get_files_in_folder(folder_path):
    async with async_playwright() as p:
        file_paths = [os.path.join(folder_path, file) for file in os.listdir(folder_path)]
        return file_paths
    
asyncio.run(main())
