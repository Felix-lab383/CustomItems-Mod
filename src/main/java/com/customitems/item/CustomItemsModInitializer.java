package com.customitems;

import net.fabricmc.api.ModInitializer;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import com.customitems.item.ModItems;

public class CustomItemsModInitializer implements ModInitializer {
    public static final Logger LOGGER = LoggerFactory.getLogger("customitems");

    @Override
    public void onInitialize() {
        LOGGER.info("Initializing Custom Items Mod...");
        
        // Register custom items
        ModItems.registerItems();
        
        LOGGER.info("Custom Items Mod initialized successfully!");
    }
}
