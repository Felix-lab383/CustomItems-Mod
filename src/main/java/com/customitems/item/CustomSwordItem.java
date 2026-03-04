package com.customitems.item;
import net.minecraft.item.SwordItem;
import net.minecraft.item.ToolMaterial;

public class CustomSwordItem extends SwordItem {
    public CustomSwordItem(ToolMaterial material, int attackDamageBonus, float attackSpeed, Settings settings) {
        super(material, attackDamageBonus, attackSpeed, settings);
    }
}