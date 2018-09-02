import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

# Set your configs
CHROME_WEBDRIVER_PATH = 'E:/My Documents/_Collections/App/chromedriver_win32/chromedriver.exe'
WEBDRIVER_WAIT_MS = 500
CHECK_INTERVAL_SECONDS = 2

PLATE_NUMBER_LIST_PATH = 'plate_numbers.txt'
ACKNOWLEDGE_URL = 'https://www.dmv.ca.gov/wasapp/ipp2/initPers.do'
PLATE_MAX_LEN = 7
PLATE_VALID_CHARS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ123456789 '


def load_plate_number_list(path):
  plate_number_list = []
  f = open(path,'r')
  for line in f.readlines():
    line = line.replace('\n', '')
    plate_number_list.append(line)
  return plate_number_list


# Returns empty string if it has invalid characters or exceeds the max length.
# Otherwise, converts letters to uppercase and fills spaces in the end.
def convert_plate_number(string):
  if len(string) > PLATE_MAX_LEN:
    return ''
  string = string.upper().ljust(PLATE_MAX_LEN)
  for c in string:
    if c not in PLATE_VALID_CHARS:
      return ''
  return string


def is_available_plate_number(driver, plate_number):
  driver.get(ACKNOWLEDGE_URL)
  WebDriverWait(driver, WEBDRIVER_WAIT_MS).until(EC.presence_of_element_located((By.NAME, 'method')))
  driver.find_element_by_id('agree').click()
  driver.find_element_by_name('method').click()

  WebDriverWait(driver, WEBDRIVER_WAIT_MS).until(EC.presence_of_element_located((By.NAME, 'plateType')))
  driver.find_element_by_id('vehicleType').send_keys('Auto')
  driver.find_element_by_id('isVehLeasedN').click()
  driver.find_element_by_name('plateType').click()
  driver.find_elements_by_tag_name('input')[20].click()

  WebDriverWait(driver, WEBDRIVER_WAIT_MS).until(EC.presence_of_element_located((By.NAME, 'plateChar6')))
  for i in range(len(plate_number)):
    driver.find_element_by_name('plateChar%d' % i).send_keys(plate_number[i])
  driver.find_elements_by_tag_name('input')[10].click()

  WebDriverWait(driver, WEBDRIVER_WAIT_MS).until(EC.presence_of_element_located((By.ID, 'footer')))
  element_step = driver.find_element_by_tag_name('legend')
  return 'Step 3: Complete Order Form' in element_step.text


if __name__ == "__main__":
  driver = webdriver.Chrome(CHROME_WEBDRIVER_PATH)
  plate_number_list = load_plate_number_list(PLATE_NUMBER_LIST_PATH)
  for plate_number in plate_number_list:
    converted_plate_number = convert_plate_number(plate_number)
    is_available = False
    if len(converted_plate_number) > 0:
      is_available = is_available_plate_number(driver, converted_plate_number)
    print('%s\t%s\t%s' % (plate_number, converted_plate_number, is_available))
    time.sleep(CHECK_INTERVAL_SECONDS)
  driver.quit()
