module SR_Util
  def self.spam_gift_change
    $game_actors[101].sp -= 
    $game_temp.battle_active_battler.absorb
    for actor in $game_party.party_actors
      if actor == $game_temp.battle_active_battler
        actor.fed = 100
        actor.promise += 100
        actor.promise += 2000 if actor.equip?("Glass Ring")
        actor.promise += 30 if actor.equip?("Trust Rune")
        actor.love += 3
        actor.love += 20 if actor.equip?("Glass Ring")
        #actor.love_dish_bonus(0)
        actor.hp = actor.maxhp if actor.equip?("Gourmet Rune")
        actor.sp = actor.maxsp if actor.equip?("Gourmet Rune")
        actor.remove_state(15)
      elsif actor != $game_actors[101]
        actor.love += 1
        actor.love += 10 if actor.equip?("Glass Ring")
        actor.promise += 10
        actor.promise += 500 if actor.equip?("Glass Ring")
        actor.promise += 5 if actor.equip?("Trust Rune")
      end
    end
  end
end