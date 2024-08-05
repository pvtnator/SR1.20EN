class Window_BoxRight < Window_Base
  def refresh
    self.contents.clear

    draw_actor_graphic(@actor, 20, 52)

    y_1 = 16
    y_2 = 188
    
    self.contents.draw_text(50, 0, 200, 24, @actor.name)
    self.contents.draw_text(50 + 24, 24, 200, 24, @actor.class_name)
    self.contents.draw_text(0, y_1 + 38, 100, 24, "Lv." + @actor.level.to_s)
    self.contents.draw_text(44, y_1 + 38, 72, 24, "【" + @actor.personality + "】", 1)
    draw_actor_state(@actor, 116, y_1 + 33, 150)
    self.contents.font.color =  normal_color
    self.contents.draw_text(20, y_1 + 92, 64, 24, "EP")
    self.contents.draw_text(20, y_1 + 120, 64, 24, "VP")
    unless @actor == $game_actors[101]
      draw_actor_fed(@actor, 20, y_1 + 148, 160)
    end

    self.contents.font.size = $default_size_mini
    draw_actor_hp(@actor, 20 + 24, y_1 + 84, 150)
    draw_actor_sp(@actor, 20 + 24, y_1 + 112, 150)
    self.contents.draw_text(0, y_1 + 64, 200, 24, "Next level: " + @actor.next_rest_exp_s + " Exp")

    
    self.contents.font.size = $default_size
    draw_actor_parameter(@actor, 0, y_2, 0, 50)
    draw_actor_parameter(@actor, 96, y_2, 1)
    draw_actor_parameter(@actor, 0, y_2 + 24, 3, 50)
    draw_actor_parameter(@actor, 96, y_2 + 24, 4)
    draw_actor_parameter(@actor, 0, y_2 + 48, 5, 50)
    draw_actor_parameter(@actor, 96, y_2 + 48, 6)
    
    x_1 = 0
    y_2 += 4
    unless @actor == $game_actors[101]
      self.contents.font.color = system_color
      self.contents.draw_text(x_1, y_2 + 72, 84, 24, "Favor")
      self.contents.draw_text(x_1 + 96, y_2 + 72, 70, 24, "Dream magic")
      self.contents.draw_text(x_1, y_2 + 96, 150, 24, "Contract beads")
      self.contents.draw_text(x_1, y_2 + 120, 84, 24, "Hunger")
      self.contents.draw_text(x_1 + 96, y_2 + 120, 84, 24, "Semen")
      self.contents.font.color = normal_color
      self.contents.draw_text(x_1 + 38, y_2 + 72, 48, 24, @actor.love.to_s, 2)
      self.contents.draw_text(x_1 + 144, y_2 + 72, 48, 24, @actor.d_power.to_s, 2)
      self.contents.draw_text(x_1 + 144 - 100, y_2 + 96, 48 + 100, 24, @actor.promise.to_s, 2)
      self.contents.draw_text(x_1 + 32, y_2 + 120, 48, 24, @actor.digest.to_s, 2)
      self.contents.draw_text(x_1 + 144, y_2 + 120, 48, 24, @actor.absorb.to_s, 2)
    end
  end
end

class Window_Base
  def draw_actor_parameter(actor, x, y, type, num_dist=60)
    case type
    when 0
      parameter_name = $data_system.words.atk
      parameter_value = actor.atk
    when 1
      parameter_name = $data_system.words.pdef
      parameter_value = actor.pdef
    when 2
      parameter_name = $data_system.words.mdef
      parameter_value = actor.mdef
    when 3
      parameter_name = $data_system.words.str
      parameter_value = actor.str
    when 4
      parameter_name = $data_system.words.dex
      parameter_value = actor.dex
    when 5
      parameter_name = $data_system.words.agi
      parameter_value = actor.agi
    when 6
      parameter_name = $data_system.words.int
      parameter_value = actor.int
    end
    self.contents.font.color = system_color
    self.contents.draw_text(x, y, 60, 32, parameter_name)
    self.contents.font.color = normal_color
    self.contents.draw_text(x + num_dist, y, 36, 32, parameter_value.to_s, 2)
  end
end

class Window_Status < Window_Base
  def refresh
    self.contents.clear

    draw_actor_graphic(@actor, 20, 52)

    y_1 = 16
    y_2 = 188
    
    self.contents.draw_text(60, 0, 200, 24, @actor.name)
    self.contents.draw_text(60 + 24, 24, 200, 24, @actor.class_name)
    self.contents.draw_text(0, y_1 + 38, 100, 24, "Lv." + @actor.level.to_s)
    self.contents.draw_text(44, y_1 + 38, 72, 24, "【" + @actor.personality + "】", 1)
    draw_actor_state(@actor, 116, y_1 + 33, 150, 0, 1)
    self.contents.font.color =  normal_color
    self.contents.draw_text(20, y_1 + 92, 64, 24, "EP")
    self.contents.draw_text(20, y_1 + 120, 64, 24, "VP")
    unless @actor == $game_actors[101]
      draw_actor_fed(@actor, 20, y_1 + 148, 160)
    end

    self.contents.font.size = $default_size_mini
    draw_actor_hp(@actor, 20 + 24, y_1 + 84, 150, 1)
    draw_actor_sp(@actor, 20 + 24, y_1 + 112, 150, 1)
    self.contents.draw_text(0, y_1 + 64, 200, 24, "Next level: " + @actor.next_rest_exp_s + " Exp")

    
    self.contents.font.size = $default_size
    draw_actor_parameter(@actor, 0, y_2, 0)
    draw_actor_parameter(@actor, 130, y_2, 1)
    draw_actor_parameter(@actor, 0, y_2 + 24, 3)
    draw_actor_parameter(@actor, 130, y_2 + 24, 4)
    draw_actor_parameter(@actor, 0, y_2 + 48, 5)
    draw_actor_parameter(@actor, 130, y_2 + 48, 6)
    

    x_1 = 274
    
    unless @actor == $game_actors[101]
      self.contents.font.color = system_color
      self.contents.draw_text(x_1, 192, 84, 24, "Favor")
      self.contents.draw_text(x_1 + 88, 192, 70, 24, "Dream magic")
      self.contents.draw_text(x_1, 216, 150, 24, "Contract beads")
      self.contents.draw_text(x_1, 240, 84, 24, "Hunger")
      self.contents.draw_text(x_1 + 88, 240, 84, 24, "Semen")
      self.contents.font.color = normal_color
      self.contents.draw_text(x_1 + 32, 192, 48, 24, @actor.love.to_s, 2)
      self.contents.draw_text(x_1 + 130, 192, 48, 24, @actor.d_power.to_s, 2)
      self.contents.draw_text(x_1 + 130 - 100, 216, 48 + 100, 24, @actor.promise.to_s, 2)
      self.contents.draw_text(x_1 + 32, 240, 48, 24, @actor.digest.to_s, 2)
      self.contents.draw_text(x_1 + 130, 240, 48, 24, @actor.absorb.to_s, 2)
    end
    
    self.contents.font.color = system_color
    self.contents.draw_text(x_1, 0, 92, 32, "Equipment")
    self.contents.font.color = normal_color
    
    equip = $data_armors[@actor.armor1_id]
    if equip != nil
      bitmap = RPG::Cache.icon($data_armors[@actor.armor1_id].icon_name)
      self.contents.blt(x_1 + 20, 20 + 4, bitmap, Rect.new(0, 0, 24, 24))
      self.contents.draw_text(x_1 + 50, 20, 150, 32, $data_armors[@actor.armor1_id].name)
    else
      self.contents.draw_text(x_1 + 25, 20, 150, 32, "---------------")
    end
  
    self.contents.font.color = system_color
    self.contents.draw_text(x_1, 44, 92, 32, "Engraved Runes")
    self.contents.font.color = normal_color
    
    rune_y = 64
    for i in 1..$data_SDB[@actor.class_id].maxrune
      if @actor.armor_id[i + 1] != 0
        bitmap = RPG::Cache.icon($data_armors[@actor.armor_id[i + 1]].icon_name)
        self.contents.blt(x_1 + 20, rune_y + 4, bitmap, Rect.new(0, 0, 24, 24))
        self.contents.draw_text(x_1 + 50, rune_y, 150, 32, $data_armors[@actor.armor_id[i + 1]].name)
      else
        self.contents.draw_text(x_1 + 25, rune_y, 150, 32, "---------------")
      end
      rune_y += 24
    end
    
    rune_y = 64
    rune_y_a = 24
    case @index
    when -2 # 非選択
      y = -100
    when 0 # 装備品
      y = 20 + 4
    when 1 # 以下ルーン
      y = rune_y + (rune_y_a * 0) + 4
    when 2
      y = rune_y + (rune_y_a * 1) + 4
    when 3
      y = rune_y + (rune_y_a * 2) + 4
    when 4
      y = rune_y + (rune_y_a * 3) + 4
    when 5
      y = rune_y + (rune_y_a * 4) + 4
    end
    self.cursor_rect.set(292, y, 170, 24)
  end
end

class Window_PromiseLeft < Window_Base
  def refresh
    self.contents.clear

    draw_actor_graphic(@actor, 20, 52)

    y_1 = 16
    y_2 = 136
    
    self.contents.draw_text(50, 0, 200, 24, @actor.name)
    self.contents.draw_text(50 + 24, 24, 200, 24, @actor.class_name)
    self.contents.draw_text(0, y_1 + 38, 100, 24, "Lv." + @actor.level.to_s)
    self.contents.draw_text(44, y_1 + 38, 72, 24, "【" + @actor.personality + "】", 1)
    draw_actor_state(@actor, 116, y_1 + 33, 150)
    self.contents.font.color =  normal_color
    self.contents.draw_text(20, y_1 + 64, 64, 24, "EP")
    self.contents.draw_text(20, y_1 + 92, 64, 24, "VP")

    self.contents.font.size = $default_size_mini
    draw_actor_hp(@actor, 20 + 24, y_1 + 56, 150)
    draw_actor_sp(@actor, 20 + 24, y_1 + 84, 150)

    self.contents.font.size = $default_size
    draw_actor_parameter(@actor, 0, y_2, 0)
    draw_actor_parameter(@actor, 106, y_2, 1)
    draw_actor_parameter(@actor, 0, y_2 + 24, 3)
    draw_actor_parameter(@actor, 106, y_2 + 24, 4)
    draw_actor_parameter(@actor, 0, y_2 + 48, 5)
    draw_actor_parameter(@actor, 106, y_2 + 48, 6)
    
    
    x_1 = 0
    y_2 += 10
    unless @actor == $game_actors[101]
      self.contents.font.color = system_color
      self.contents.draw_text(x_1, y_2 + 72, 84, 24, "Favor")
      self.contents.draw_text(x_1 + 98, y_2 + 72, 70, 24, "Dream magic")
      self.contents.draw_text(x_1, y_2 + 96, 84, 24, "Hunger")
      self.contents.draw_text(x_1 + 98, y_2 + 96, 84, 24, "Semen")
      self.contents.draw_text(264, 10, 150, 24, "Contract beads")
      self.contents.font.color = normal_color
      self.contents.draw_text(x_1 + 32, y_2 + 72, 48, 24, @actor.love.to_s, 2)
      self.contents.draw_text(x_1 + 144, y_2 + 72, 48, 24, @actor.d_power.to_s, 2)
      self.contents.draw_text(x_1 + 32, y_2 + 96, 48, 24, @actor.digest.to_s, 2)
      self.contents.draw_text(x_1 + 144, y_2 + 96, 48, 24, @actor.absorb.to_s, 2)
      self.contents.draw_text(446 - 100, 10, 84 + 100, 24, @actor.promise.to_s, 2)
    end
  end
end

class Window_Cook_Recipe < Window_Base
  def draw_dish_effect(index)
    x = 10
    y = index * 20 + 192
    
    # オリジナルにあるものは文字色を変えない
    color_change = true
    for ori_effect in @original_dish.effect
      color_change = false if @dish.effect[index].check == ori_effect.check
    end
    self.contents.font.color = normal_color
    self.contents.font.color = text_color(3) if color_change
    self.contents.font.color = text_color(2) if @dish.effect[index].level < 0

    self.contents.draw_text(x, y, 250, 40, @dish.effect_text(@dish.effect[index]))
  end
end

class Window_Cook_Cooking < Window_Base
  def refresh
    self.contents.clear
    self.contents.font.size = $default_size
    self.contents.font.color = normal_color
    
    draw_actor_graphic(@actor, 30, 52)
    
    self.contents.draw_text(60, 0, 200, 24, @actor.name)
    self.contents.draw_text(60 + 24, 24, 200, 24, @actor.class_name)
    self.contents.draw_text(10, 54, 40, 24, "Lv." + @actor.level.to_s, 1)
    self.contents.draw_text(80, 47 - 2, 60, 32, "VP")
    draw_actor_parameter(@actor, 10, 80, 4)
    self.contents.font.size = $default_size_mini
    draw_actor_sp(@actor, 80, 47, 144, 1)

    y_0 = 95
    y_plus1 = 20
    
    self.contents.draw_text(0, 105, 150, 32, "<<Cooking correction>>")

    # 補正の確認
    @bonus = @actor.cook_bonus
    for i in 0...@bonus.size
      draw_bonus(i)
    end
    
    self.contents.font.size = $default_size
    self.contents.font.color = system_color
    self.contents.draw_text(5, 215, 100, 32, "Skill:")
    self.contents.draw_text(120, 215, 100, 32, "Great: ")
    self.contents.draw_text(122, 215, 100, 32, "％", 2)
    self.contents.font.color = normal_color
    self.contents.draw_text(5, 215, 100, 32, @actor.cook_dex.to_s, 2)
    self.contents.draw_text(105, 215, 100, 32, @actor.critical_cook_persent(@dish).to_s, 2)
    
    draw_speech
  end
end

class Window_SystemLeft < Window_Base
  def refresh
    self.contents.clear
    self.contents.font.color = normal_color  

    row_refresh
    
    x = 50
    y = 0
    y_a = 32
    
    self.contents.font.color = crisis_color
    self.contents.font.size = 22
    self.contents.draw_text(x + 168, y + (y_a * 0), 200, 24, "Map settings")
    #
    self.contents.font.color = normal_color  
    self.contents.font.size = $default_size
    self.contents.draw_text(x, y + (y_a * 1), 200, 24, "Default movement")
    self.contents.draw_text(x, y + (y_a * 2), 200, 24, "Semen Offering")
    self.contents.draw_text(x, y + (y_a * 3), 200, 24, "Port priority")
    self.contents.draw_text(x, y + (y_a * 4), 200, 24, "Ally satiety")
    #
    self.contents.font.color = crisis_color
    self.contents.font.size = 22
    self.contents.draw_text(x + 168, y + (y_a * 5), 200, 24, "Battle settings")
    #
    self.contents.font.color = normal_color  
    self.contents.font.size = $default_size
    self.contents.draw_text(x, y + (y_a * 6), 200, 24, "Battle speed")
    self.contents.draw_text(x, y + (y_a * 7), 200, 24, "Message mode")
    self.contents.draw_text(x, y + (y_a * 8), 200, 24, "Resist time")
    self.contents.draw_text(x, y + (y_a * 9), 200, 24, "Semen graphics")
    self.contents.draw_text(x, y + (y_a * 10), 200, 24, "Cursor memory")
    self.contents.draw_text(x, y + (y_a * 11), 200, 24, "Erotic Message")
    #
    self.contents.font.color = crisis_color
    self.contents.font.size = 22
    self.contents.draw_text(x + 184, y + (y_a * 12), 200, 24, "Other")
    #
    self.contents.font.color = normal_color  
    self.contents.font.size = $default_size
    self.contents.draw_text(x, y + (y_a * 13), 200, 24, "Full screen switch")    
    self.contents.draw_text(x, y + (y_a * 14), 200, 24, "Suspend game")    

    self.cursor_rect.set(x - 4, y - 4 + (y_a * @index) - self.oy, 130, 32)
   
    
    x = 270
    #●デフォルト移動
    x_a = 48
    color_change(1, false)
    self.contents.draw_text(x, y + (y_a * 1), 200, 24, "Walk")
    color_change(1, true)
    self.contents.draw_text(x + x_a, y + (y_a * 1), 200, 24, "Dash")
    #●精の献上
    x_a = 48
    color_change(2, true)
    self.contents.draw_text(x, y + (y_a * 2), 200, 24, "View")
    color_change(2, false)
    self.contents.draw_text(x + x_a, y + (y_a * 2), 200, 24, "Hide")
    #●ポート設定
    x_a = 84
    color_change(3, false)
    self.contents.draw_text(x, y + (y_a * 3), 200, 24, "Save")
    color_change(3, true)
    self.contents.draw_text(x + x_a, y + (y_a * 3), 200, 24, "Teleport")
    #●空腹度
    x_a = 56
    color_change(4, 0)
    self.contents.draw_text(x + (x_a * 0), y + (y_a * 4), 200, 24, "Normal")
    color_change(4, 1)
    self.contents.draw_text(x + (x_a * 1), y + (y_a * 4), 200, 24, "Slower")
    color_change(4, 2)
    self.contents.draw_text(x + (x_a * 2), y + (y_a * 4), 200, 24, "Slowest")
    #●バトルスピード
    x_a = 52
    color_change(6, 0)
    self.contents.draw_text(x + (x_a * 0), y + (y_a * 6), 200, 24, "Slow")
    color_change(6, 1)
    self.contents.draw_text(x + (x_a * 1 - 6), y + (y_a * 6), 200, 24, "Normal")
    color_change(6, 2)
    self.contents.draw_text(x + (x_a * 2), y + (y_a * 6), 200, 24, "Fast")
    #●メッセージモード
    x_a = 84
    color_change(7, 0)
    self.contents.draw_text(x + (x_a * 0), y + (y_a * 7), 200, 24, "Manual")
    color_change(7, 1)
    self.contents.draw_text(x + (x_a * 1 - 10), y + (y_a * 7), 200, 24, "Semi-auto")
    color_change(7, 2)
    self.contents.draw_text(x + (x_a * 2), y + (y_a * 7), 200, 24, "Full-auto")
    #●レジスト猶予期間
    x_a = 52
    color_change(8, 0)
    self.contents.draw_text(x + (x_a * 0), y + (y_a * 8), 200, 24, "Short")
    color_change(8, 1)
    self.contents.draw_text(x + (x_a * 1), y + (y_a * 8), 200, 24, "Normal")
    color_change(8, 2)
    self.contents.draw_text(x + (x_a * 2 + 6), y + (y_a * 8), 200, 24, "Long")
    color_change(8, 3)
    self.contents.draw_text(x + (x_a * 3), y + (y_a * 8), 200, 24, "Chill")
    #●精液グラフィック表示
    x_a = 48
    color_change(9, true)
    self.contents.draw_text(x, y + (y_a * 9), 200, 24, "Show")
    color_change(9, false)
    self.contents.draw_text(x + x_a, y + (y_a * 9), 200, 24, "Skip")
    #●カーソル位置記憶
    x_a = 48
    color_change(10, true)
    self.contents.draw_text(x, y + (y_a * 10), 200, 24, "Yes")
    color_change(10, false)
    self.contents.draw_text(x + x_a, y + (y_a * 10), 200, 24, "No")
    #●エロティックメッセージ
    x_a = 56
    color_change(11, 0)
    self.contents.draw_text(x, y + (y_a * 11), 200, 24, "Simple")
    color_change(11, 1)
    self.contents.draw_text(x + x_a, y + (y_a * 11), 200, 24, "Normal")
    color_change(11, 2)
    self.contents.draw_text(x + (x_a * 2), y + (y_a * 11), 200, 24, "Detailed")
  end
end