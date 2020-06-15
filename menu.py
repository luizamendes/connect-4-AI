import pygame

branco = (255,255,255)
preto = (0,0,0)
vermelho = (255,00,0)
verde = (0,255,0)
azul = (0,0,255)

try:
	pygame.init()
	pygame.font.init()
except:
	print("O modulo pygame não foi inicializado com sucesso")

largura = 640
altura = 480

fundo = pygame.display.set_mode((largura,altura))

pygame.display.set_caption('Connect 4')

sair = True

menu_choices = {'choice_1': 0, 'choice_2': 0}

menu_step_font = pygame.font.SysFont("comicsansms", 50)
font = pygame.font.SysFont("comicsansms", 30)

choice_1_text = ''
choice_1_text_render = font.render(choice_1_text, True, azul)

choice_2_text = ''
choice_2_text_render = font.render(choice_2_text, True, azul)

menu_step_text = "Modo de Jogo"
menu_step_text_render = menu_step_font.render(menu_step_text, True, azul)

text_1 = "1 - AI contra AI"
text_2 = "2 - Humano contra AI"
text_1_render = font.render(text_1, True, vermelho)
text_2_render = font.render(text_2, True, vermelho)

start_game_text = 'Aperte o Enter para começar'
start_game_text_render = font.render(start_game_text, True, preto)

AI_X_AI_flag = False
next_step = 0

while sair:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sair = False
	
	fundo.fill(branco)
	fundo.blit(menu_step_text_render, (200, 100))
	fundo.blit(text_1_render,(200, 170))
	fundo.blit(text_2_render,(200, 200))

	if event.type == pygame.KEYDOWN:# 1=49, 2=50
		if next_step == 0:
			if event.key == 49:
				menu_choices['choice_1'] = 1
			if event.key == 50:
				menu_choices['choice_1'] = 2
				next_step = 1
			if event.key == 13:
				from connectFour import start
				start(menu_choices['choice_1'])

		elif next_step == 1:
    		if event.key == 51:
    			menu_choices['choice_2'] = 1
                next_step = 2      
            if event.key == 52:
                menu_choices['choice_2'] = 2
                next_step = 2

        elif next_step == 2:
            if event.key == 53:
                menu_choices['choice_3'] = 1
                next_step = 3      
            if event.key == 54:
                menu_choices['choice_3'] = 2
                next_step = 3
        
        elif next_step == 3:
            if event.key == 13:
                from connectFour import start
                start(menu_choices['choice_1'], menu_choices['choice_2'], menu_choices['choice_3'])

	if menu_choices['choice_1'] == 1:
		choice_1_text = 'Modo: AI contra AI'
		fundo.blit(start_game_text_render, (180, 300))
		choice_1_text_render = font.render(choice_1_text, True, azul)
		fundo.blit(choice_1_text_render,(220, 230))
		text_1_render = font.render(text_1, True, branco)
		text_2_render = font.render(text_2, True, branco)

	if next_step == 1:
		if menu_choices['choice_1'] == 2:
			choice_1_text = 'Humano contra AI'
			menu_step_text = "Nível de Dificuldade"
			menu_step_text_render = menu_step_font.render(menu_step_text, True, azul)
			text_1 = '3 - Fácil'
			text_2 = '4 - Difícil'
			text_1_render = font.render(text_1, True, vermelho)
			text_2_render = font.render(text_2, True, vermelho)
		choice_1_text_render = font.render(choice_1_text, True, azul)
		fundo.blit(choice_1_text_render,(200, 300))
	
	if next_step == 2:
        if menu_choices['choice_1'] == 2:
            choice_1_text = 'Humano contra AI'
            menu_step_text = "Contra qual IA?"
            menu_step_text_render = menu_step_font.render(menu_step_text, True, azul)
            text_1 = '5 - Com poda alfa beta pruning'
            text_2 = '6 - Sem poda alfa beta pruning'
            text_1_render = font.render(text_1, True, vermelho)
            text_2_render = font.render(text_2, True, vermelho)
        choice_1_text_render = font.render(choice_1_text, True, azul)
        fundo.blit(choice_1_text_render,(200, 300))
    
    if next_step == 3:
        if menu_choices['choice_2'] == 1:
            choice_2_text = 'Nível fácil'
        if menu_choices['choice_2'] == 2:
            choice_2_text = 'Nível difícil'
        fundo.blit(start_game_text_render, (180, 300))
        choice_2_text_render = font.render(choice_2_text, True, azul)
        fundo.blit(choice_1_text_render,(220, 230))
        fundo.blit(choice_2_text_render,(220, 260))
        text_1_render = font.render(text_1, True, branco)
        text_2_render = font.render(text_2, True, branco)
					
	pygame.display.update()
	
pygame.quit()
quit()