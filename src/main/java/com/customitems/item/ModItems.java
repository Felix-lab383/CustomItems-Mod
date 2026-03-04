package com.customitems.item;

import net.minecraft.item.Item;
import net.minecraft.item.ToolMaterials;
import net.minecraft.registry.Registries;
import net.minecraft.registry.Registry;
import net.minecraft.util.Identifier;

public class ModItems {
    // Custom Tool Items - Ruby Tools (Diamond tier)
    public static final Item RUBY_PICKAXE = registerItem("ruby_pickaxe", 
        new CustomPickaxeItem(ToolMaterials.DIAMOND, 1, -2.8f, new Item.Settings()));
    
    public static final Item RUBY_SHOVEL = registerItem("ruby_shovel",
        new CustomShovelItem(ToolMaterials.DIAMOND, 1.5f, -3.0f, new Item.Settings()));
    
    public static final Item RUBY_AXE = registerItem("ruby_axe",
        new CustomAxeItem(ToolMaterials.DIAMOND, 6.0f, -3.2f, new Item.Settings()));
    
    public static final Item RUBY_SWORD = registerItem("ruby_sword",
        new CustomSwordItem(ToolMaterials.DIAMOND, 3, -2.4f, new Item.Settings()));
    
    // Custom Tool Items - Emerald Tools (Netherite tier)
    public static final Item EMERALD_PICKAXE = registerItem("emerald_pickaxe",
        new CustomPickaxeItem(ToolMaterials.NETHERITE, 1, -2.8f, new Item.Settings()));
    
    public static final Item EMERALD_SHOVEL = registerItem("emerald_shovel",
        new CustomShovelItem(ToolMaterials.NETHERITE, 1.5f, -3.0f, new Item.Settings()));

    private static Item registerItem(String name, Item item) {
        return Registry.register(Registries.ITEM, new Identifier("customitems", name), item);
    }

    public static void registerItems() {
        // Items are registered via the static initializers above
    }
}
