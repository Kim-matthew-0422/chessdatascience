# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import re
import pandas as pd
from stockfish import Stockfish
import chess
from selenium.webdriver.common.action_chains import ActionChains


    
cols = ['Player', 'Movecount', 'Moves','opponentmoves', 'Eval-bar', 'Color','gamecount','opening','type']
df = pd.DataFrame(columns=cols)
game_count = 1
board_play = chess.Board()
move_count = 1
current_color = ''


stockfish = Stockfish('/Users/mat_c/Desktop/Chess.com-Bot-main/stockfish.exe')
driver = webdriver.Chrome('/Users/mat_c/Downloads/chromedriver.exe')
driver.get("https://www.chess.com/play/computer")


def scroll():
    action = ActionChains(driver)
    scroll = driver.find_elements_by_xpath('//*[@id="board-layout-sidebar"]/div/section/div/div/div[1]/div/div[2]/div[3]/div/img')
    action.move_to_element(scroll[0]).move_by_offset(0,0).click().perform()
    action.move_to_element(scroll[0]).move_by_offset(0,0).send_keys(Keys.SPACE).perform()
    action.move_to_element(scroll[0]).move_by_offset(0,0).send_keys(Keys.SPACE).perform()
    time.sleep(4)
    
    
mainboard = driver.find_elements_by_xpath('//*[@id="board-layout-chessboard"]')
game_over= driver.find_elements_by_xpath('//*[@id="game-over-modal"]/div/div[2]/div/div[1]/div[2]')
driver_size = driver.get_window_size()
#remove ad
time.sleep(1)
exit_ad = driver.find_elements_by_xpath('//div[@class = "icon-font-chess x ui_outside-close-icon"]')
exit_ad[0].click()
#remove choose button click
time.sleep(1)
scroll()
bot_choice = driver.find_elements_by_xpath('//*[@id="board-layout-sidebar"]/div/section/div/div/div[8]/div/div[2]/div[1]/div')
bot_choice[0].click()
choose_btn = driver.find_elements_by_xpath('//*[@id="board-layout-sidebar"]/div/div[2]/button')
choose_btn[0].click()
time.sleep(1)
play_as = driver.find_elements_by_xpath('//*[@id="board-layout-sidebar"]/div/section/div/div[1]/div[2]')
play_as[0].click()
time.sleep(1)
play_btn = driver.find_elements_by_xpath('//*[@id="board-layout-sidebar"]/div/div[2]/button')
play_btn[0].click()

game_count = 0

board_color = driver.find_elements_by_xpath('//*[@id="board-vs-personalities"]')[0].text[0]

board = driver.execute_script('''
  function coords(elem){
      var n = elem.getBoundingClientRect()
      return {top:n.top, left:n.left, width:n.width, height:n.height}
  }
  var pieces = []
  for (var i = 1; i < 9; i++){
     if (i > 6 || i < 3){
        pieces.push(Array.from((new Array(8)).keys()).map(function(x){
           var square = document.querySelector(`.piece.square-${x+1}${i}`)
           return {...coords(square), piece:square.getAttribute('class').split(' ')[1]}
        }));
     }
     else{
        pieces.push(Array.from((new Array(8)).keys()).map(function(x){
           var arr = pieces[pieces.length-1]
           return {left:arr[x].left, top:arr[x].top - arr[x].height, 
             width:arr[x].width, height:arr[x].height, piece:null}
        }));
     }
  }
  return pieces
''')[::-1]

offset_x = mainboard[0].size.get('width') / 846
offset_y = mainboard[0].size.get('height') / 786


# if screen size is not 1936/1048, make sure the multiply all by offset_x, offset_y


player_color = ''

     
        

def click_square(x):
   elem = driver.execute_script('''return document.querySelector('body')''')
   ac = ActionChains(driver)
   ac.move_to_element(elem).move_by_offset(letters.get(x[0]),numbers.get(x[1])).click().perform()

        




#-650 - 100 x, 390 - -390 y @ 1936, 1048
#-530 - 100 x, 240 - -380 y @ 1265, 1029
# 846/786 if screen size is bigger than -> switch these values @ 1936 by 1048

# make the first move

for i in range(50):
    
    color_check = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//*[@id="board-vs-personalities"]'))).get_attribute('class')  
    if color_check == 'board flipped':
        current_color = 'bp'
        letters = {'h': -650 * offset_x, 'g': -556.25, 'f': -462.5, 'e': -328.75, 'd': -255, 'c': -161.25, 'b': -67.5, 'a': 46.25}
        numbers = {'8': 390, '7' : 292.5, '6': 195, '5': 97.5, '4': -20, '3': -127.5, '2':-210, '1': -315.5}
        first_move = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//*[@id="board-layout-sidebar"]/div/vertical-move-list/div/div'))).get_attribute('textContent')
       
        board_play.push_san(first_move)
        stockfish.set_fen_position(board_play.fen())
        stockfish.get_evaluation()
        bestest = stockfish.get_best_move()
        board_play.push_san(bestest)
        # mimic the move on chess.com
        
        temp_str = []


        player = driver.find_elements_by_xpath('//*[@id="board-layout-player-top"]/div/div/div/div/div[1]/div/span[1]')[0].text
        temp_str.insert(0, player)
        temp_str.insert(1, 1)


        click_square(bestest[0:2])
        click_square(bestest[2:4])
        move_count = 2


        first_move = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//*[@id="board-layout-sidebar"]/div/vertical-move-list/div/div'))).get_attribute('textContent')
        temp_str.insert(2, first_move)
        temp_str.insert(3, bestest)
        temp_str.insert(4, stockfish.get_evaluation()['value'])
        temp_str.insert(5, current_color)
        temp_str.insert(6, game_count)
        
        temp_str.insert(7, ' ')
        temp_str.insert(8, stockfish.get_evaluation()['type'])
        temp_df = pd.DataFrame([temp_str], columns=cols)
        df = df.append(temp_df)
        game_counter = 0
    else:
            letters = {'a': -650 * offset_x, 'b': -556.25, 'c': -462.5, 'd': -328.75, 'e': -255, 'f': -161.25, 'g': -67.5, 'h': 46.25}
            numbers = {'1': 390, '2' : 292.5, '3': 195, '4': 97.5, '5': -20, '6': -127.5, '7':-210, '8': -315.5}
            stockfish.set_fen_position(board_play.fen())
            bestest = stockfish.get_best_move()
            board_play.push_san(bestest)
            current_color = 'wp'
            
            temp_str = []
        
        
            player = driver.find_elements_by_xpath('//*[@id="board-layout-player-top"]/div/div/div/div/div[1]/div/span[1]')[0].text
            temp_str.insert(0, player)
            temp_str.insert(1, 1)
        
        
            click_square(bestest[0:2])
            click_square(bestest[2:4])
            
            stockfish.set_fen_position(board_play.fen())

            move_count = 2
            
        
            first_move = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//*[@id="board-layout-sidebar"]/div/vertical-move-list/div[1]/div[2]'))).get_attribute('textContent')
            temp_str.insert(2, '')
            temp_str.insert(3, bestest)
            temp_str.insert(4, stockfish.get_evaluation()['value'])
            temp_str.insert(5, current_color)
            temp_str.insert(6, game_count)

            temp_str.insert(7, ' ')
            temp_str.insert(8, stockfish.get_evaluation()['type'])
            temp_df = pd.DataFrame([temp_str], columns=cols)
            df = df.append(temp_df)
            temp_str = []
    

            current_move = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//*[@id="board-layout-sidebar"]/div/vertical-move-list/div/div[2]'))).get_attribute('textContent')
            board_play.push_san(current_move)
            stockfish.set_fen_position(board_play.fen())
            stockfish.get_evaluation()
            
            
            temp_str.insert(0, player)
            temp_str.insert(1, 2)
            temp_str.insert(2, first_move)
            temp_str.insert(3, bestest)
            bestest = stockfish.get_best_move()
            click_square(bestest[0:2])
            click_square(bestest[2:4])
            board_play.push_san(bestest)
            stockfish.set_fen_position(board_play.fen())
            stockfish.get_evaluation()
            temp_str.insert(4, stockfish.get_evaluation()['value'])
            temp_str.insert(5, current_color)
            temp_str.insert(6, game_count)

            temp_str.insert(7, ' ')
            temp_str.insert(8, stockfish.get_evaluation()['type'])
            temp_df = pd.DataFrame([temp_str], columns=cols)
            df = df.append(temp_df)
            
    while len(game_over) == 0:
        opening = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//*[@id="board-layout-sidebar"]/div/eco-opening/span'))).get_attribute('textContent')
        temp_str = []
        
        if current_color == 'bp':
            
            current_move = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//*[@id="board-layout-sidebar"]/div/vertical-move-list/div['  + str(move_count) + ']/div'))).get_attribute('textContent')
            
            try:
                board_play.push_san(current_move)
                stockfish.set_fen_position(board_play.fen())
                stockfish.get_evaluation()
            except:
                break
        else: 
                current_move = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//*[@id="board-layout-sidebar"]/div/vertical-move-list/div['+ str(move_count) +']/div[2]'))).get_attribute('textContent')
                opponent_move = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//*[@id="board-layout-sidebar"]/div/vertical-move-list/div['  + str(move_count) + ']/div'))).get_attribute('textContent')
                try:
                    board_play.push_san(current_move)
                    stockfish.set_fen_position(board_play.fen())
                    stockfish.get_evaluation()
                except:
                    break

        print(current_move)
        try:
            best_move = stockfish.get_best_move()
            click_square(best_move[0:2])
            click_square(best_move[2:4])
        except:
            continue
        
        try:
            promot = driver.find_element_by_xpath("//div[contains(@class, 'promotion-piece wq')]")
            promot.click()
        except:
            print('white-no-promote')
        try:
            promot = driver.find_element_by_xpath("//div[contains(@class, 'promotion-piece bq')]")
            promot.click()
        except:
            print('black-no-promote')
        if current_color == 'bp':
            
            opponent_move = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//*[@id="board-layout-sidebar"]/div/vertical-move-list/div['  + str(move_count) + ']/div[2]'))).get_attribute('textContent')
        try:
            board_play.push_san(best_move)
        except:
            continue
        game_over = driver.find_elements_by_xpath('//*[@id="game-over-modal"]/div/div[2]/div/div[1]/div[2]')
        
        move_count = move_count + 1
        temp_str.insert(0, player)
        temp_str.insert(1, move_count)
        temp_str.insert(2, current_move)
        temp_str.insert(3, opponent_move)
        temp_str.insert(4, stockfish.get_evaluation()['value'])
        temp_str.insert(5, current_color)
        temp_str.insert(6, game_count)
        
        evalu = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//*[@id="board-layout-sidebar"]/div/div[1]/div[2]/div[1]/div/div[2]/div[1]/div'))).get_attribute('textContent')

        temp_str.insert(7, opening)
        temp_str.insert(8, stockfish.get_evaluation()['type'])
        temp_df = pd.DataFrame([temp_str], columns=cols)
        df = df.append(temp_df)
        game_over= driver.find_elements_by_xpath('//*[@id="game-over-modal"]/div/div[2]/div/div[1]/div[2]')
        if len(game_over) > 0:
            break
            print('game_over')
     
    
    
    time.sleep(1)
    new_game = driver.find_elements_by_xpath('//*[@id="board-layout-sidebar"]/div/div[3]/div[1]/button[2]')
    time.sleep(1)
    new_game[0].click()
    time.sleep(1)
    choose_new = driver.find_elements_by_xpath('//*[@id="board-layout-sidebar"]/div/div[2]/button')
    choose_new[0].click()
    time.sleep(1)
    shuffle_1 = driver.find_elements_by_xpath('//*[@id="select-playing-as-radio-king-stroke"]')
    shuffle_1[0].click()
    shuffle_2 = driver.find_elements_by_xpath('//*[@id="board-layout-sidebar"]/div/section/div/div[1]/div[2]')
    shuffle_2[0].click()
    play_new = driver.find_elements_by_xpath('//*[@id="board-layout-sidebar"]/div/div[2]/button')
    play_new[0].click()
    game_over= driver.find_elements_by_xpath('//*[@id="game-over-modal"]/div/div[2]/div/div[1]/div[2]')
    game_count = game_count + 1
    board_play.reset()
    df.to_excel(r''+player + '.xlsx', index=False, header=True)