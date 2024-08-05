class Sprite_Battler < RPG::Sprite
  def change_Bitmap_Data()
    @battler_data.originName = @battler.battler_name
    @battler_data.baseName = @battler_data.originName.clone()
    bmp_name = []
    bmp_name[0] = @battler_data.baseName + "_I"
    bmp_name[1] = @battler_data.baseName + "_L"
    bmp_name[2] = @battler_data.baseName + "_M"
    bmp_name[3] = @battler_data.baseName + "_N"
    bmp_name[4] = @battler_data.baseName + "_I2"
	bmp_name[5] = @battler_data.baseName + "_A"
	bmp_name[6] = @battler_data.baseName + "_PZ"
	bmp_name[7] = @battler_data.baseName + "_OI"
	
	common_enemies = 0
	for enemy in $game_troop.enemies
      if enemy.exist?
        common_enemies += 1 unless enemy.boss_graphic?
      end
    end
	
    # 本気インサートの場合、インサート記号をつける
    if @battler.earnest_vagina_insert? and RPG::Cache.battler_exist?(bmp_name[4])
      @battler_data.baseName = bmp_name[4]
    # インサートの場合、インサート記号をつける
	elsif @battler.vagina_insert? and RPG::Cache.battler_exist?(bmp_name[5]) and (common_enemies==1 or @battler.boss_graphic?) and @battler.initiative_level > 0 
      @battler_data.baseName = bmp_name[5]
    elsif @battler.vagina_insert? and RPG::Cache.battler_exist?(bmp_name[0]) and (common_enemies==1 or @battler.boss_graphic?)
      @battler_data.baseName = bmp_name[0]
	elsif @battler.paizuri? and RPG::Cache.battler_exist?(bmp_name[6]) and (common_enemies==1 or @battler.boss_graphic?)
	  @battler_data.baseName = bmp_name[6]
	elsif @battler.penis_oralsex? and RPG::Cache.battler_exist?(bmp_name[7]) and (common_enemies==1 or @battler.boss_graphic?)
	  @battler_data.baseName = bmp_name[7]
    # 挿入不可半裸の場合、挿入不可半裸記号をつける
    elsif @battler.uninsertable_half_nude? and RPG::Cache.battler_exist?(bmp_name[1])
      @battler_data.baseName = bmp_name[1]
    # 挿入可能半裸の場合、挿入可能半裸記号をつける
    elsif @battler.insertable_half_nude? and RPG::Cache.battler_exist?(bmp_name[2])
      @battler_data.baseName = bmp_name[2]
    # 全裸の場合、全裸記号をつける
    elsif @battler.full_nude? and RPG::Cache.battler_exist?(bmp_name[3])
      @battler_data.baseName = bmp_name[3]
    end
    
    # クライシスの場合、クライシス記号をつける
    bmp_name[0] = @battler_data.baseName + "_C"
    bmp_name[1] = @battler_data.originName + "_C"
    if @battler.crisis_graphic? and RPG::Cache.battler_exist?(bmp_name[0])
      @battler_data.crysisName = bmp_name[0]
    elsif @battler.crisis_graphic? and RPG::Cache.battler_exist?(bmp_name[1])
      @battler_data.crysisName = bmp_name[1]
    else
      @battler_data.crysisName = nil
    end
    
    # 精液がかかっている場合、その精液箇所をつける
    # ただし精液処理のスイッチが入ってる場合のみ
    if $game_system.system_sperm == true
      bmp_name[0] = @battler_data.baseName + "__"
      bmp_name[1] = @battler_data.originName + "__"
      if @battler.crisis_graphic? 
        bmp_name[2] = @battler_data.crysisName + "__"
      end
      if @battler.state?(9) or @battler.state?(10)
        # ぶっかけ
        if @battler.state?(9)
          bmp_name[0] += "S"
          bmp_name[1] += "S"
          if @battler.crisis_graphic? 
            bmp_name[2] += "S"
          end
        end
        # 中出し
        if @battler.state?(10)
          bmp_name[0] += "Z"
          bmp_name[1] += "Z"
          if @battler.crisis_graphic? 
            bmp_name[2] += "Z"
          end
        end
        if @battler.crisis_graphic? and RPG::Cache.battler_exist?(bmp_name[2])
          @battler_data.samenName = bmp_name[2]
        elsif RPG::Cache.battler_exist?(bmp_name[0])
          @battler_data.samenName = bmp_name[0]
        elsif RPG::Cache.battler_exist?(bmp_name[1])
          @battler_data.samenName = bmp_name[1]
        end
      else
        @battler_data.samenName = nil
      end
    end
    # ファイル名か色相が現在のものと異なる場合
    if @battler_data.change?() or
       @battler_hue != @battler.battler_hue
      
      #ベースデータに変動あり
      if @battler_data.last_baseName != @battler_data.baseName
        # ビットマップを取得、設定
        @battler_data.last_baseName = @battler_data.baseName
        @battler_hue = @battler.battler_hue
        self.bitmap = RPG::Cache.battler(@battler_data.baseName, @battler_hue).clone()
        @width = self.bitmap.width
        @height = self.bitmap.height
        self.ox = @width / 2
        self.oy = @height
        # 戦闘不能または隠れ状態なら不透明度を 0 にする
        if @battler.dead? or @battler.hidden
          self.opacity = 0
        end
        @battler_BMP_Manager = BitmapBlendManager.new(self.bitmap)
      else
        #変動ない場合はブレンドクリアのみ
        @battler_BMP_Manager.blendClear()
      end
      
      if @battler_data.crysisName != nil
        #クライシス画像ブレンド
        blendBitmap = RPG::Cache.battler(@battler_data.crysisName, @battler_hue).clone()
        @battler_BMP_Manager.blt(blendBitmap, 0, 0)
      end
      @battler_data.last_crysisName = @battler_data.crysisName
      
      #精液画像ブレンド
      if @battler_data.samenName != nil
        blendBitmap = RPG::Cache.battler(@battler_data.samenName, @battler_hue).clone()
        @battler_BMP_Manager.blt(blendBitmap, 0, 0)
      end
      @battler_data.last_samenName = @battler_data.samenName
    end
    
  end
end

module SR_Util
  def self.gift_graphic_make1(actor)
    $sprite = Sprite.new
    name = actor.battler_name
    name = actor.battler_name + "_N" if $game_switches[177]
    if $game_switches[178]
	  if RPG::Cache.battler_exist?(actor.battler_name + "_A")
        name = actor.battler_name + "_A" 
      elsif RPG::Cache.battler_exist?(actor.battler_name + "_I")
        name = actor.battler_name + "_I" 
      else
        name = actor.battler_name + "_N"
      end
    end
    $game_temp.gift_graphic = name
    graphic = RPG::Cache.battler($game_temp.gift_graphic,actor.battler_hue)
    $sprite.bitmap = Bitmap.new(graphic.width, graphic.height)
    $sprite.bitmap.blt(0, 0, graphic, Rect.new(0, 0, graphic.width, graphic.height), 255)
    $sprite.x = 320
    $sprite.y = 240
    $sprite.y += 60 if actor.boss_graphic?
    $sprite.ox = $sprite.bitmap.width / 2
    $sprite.oy = $sprite.bitmap.height / 2
    $sprite.opacity = 0
  end
end