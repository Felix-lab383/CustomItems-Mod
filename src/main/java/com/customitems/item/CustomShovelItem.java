package com.customitems.item;
import net.minecraft.item.ShovelItem;
import net.minecraft.item.ToolMaterial;

public class CustomShovelItem extends ShovelItem {
    public CustomShovelItem(ToolMaterial material, float attackDamageBonus, float attackSpeed, Settings settings) {
        super(material, attackDamageBonus, attackSpeed, settings);
    }
}