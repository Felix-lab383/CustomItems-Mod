package com.customitems.item;

import net.minecraft.item.PickaxeItem;
import net.minecraft.item.ToolMaterial;

public class CustomPickaxeItem extends PickaxeItem {
    public CustomPickaxeItem(ToolMaterial material, int attackDamageBonus, float attackSpeed, Settings settings) {
        super(material, attackDamageBonus, attackSpeed, settings);
    }
}
