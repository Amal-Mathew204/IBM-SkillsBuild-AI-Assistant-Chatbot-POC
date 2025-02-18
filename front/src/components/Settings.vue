<template>
  <div class="settings">
    <h1>Settings:</h1>
    <!-- Font Size Selector -->
    <div class="settingsValues">
      <h3><strong>Font Size:</strong></h3>
      <div class="fontSizeSetting">
        <input type="range" min="12" max="32" v-model="fontSize" @input="updateSettings"/>
        <label class="fontSizeValue">{{ fontSize }}px</label>
      </div>
    </div>
    <!-- Font Colour Selector-->
    <div class="settingsValues">
      <h3><strong>Font Colour:</strong></h3>
      <div class="colorSetting">
        <input type="color" v-model="fontColor" @input="updateSettings" />
        <div class="colorDisplay">
          {{ fontColor }}
        </div>
      </div>
    </div>
    <!-- Background Colour Selector-->
    <div class="settingsValues">
      <h3><strong>Background Colour:</strong></h3>
      <div class="colorSetting">
        <input type="color" v-model="backgroundColor" @input="updateSettings" />
        <div class="colorDisplay">
          {{ backgroundColor }}
        </div>
      </div>
    </div>
    <!-- Reset Button -->
    <div class="resetButtonContainer">
      <button @click="resetSettings" class="resetButton">Reset to Default</button>
    </div>
  </div>
</template>

<script>
export default {
  name: "ChatbotSettings",
  data() {
    // Default values
    return {
      fontSize: 16,
      fontColor: "#000000",
      backgroundColor: "#ffffff",
    };
  },
  mounted() {
    // Fetches saved setting from local storage 
    const savedSettings = JSON.parse(localStorage.getItem("chatbotSettings"));
    // Apply saved settings from local storage if there is any saved
    if (savedSettings) {
      this.fontSize = savedSettings.fontSize;
      this.fontColor = savedSettings.fontColor;
      this.backgroundColor = savedSettings.backgroundColor;
      this.updateSettings();
    } 
  },
  methods: {
    // This method updates the setting
    updateSettings() {
      // Sets new setting value
      const newSettings = {
        fontSize: `${this.fontSize}px`,  
        color: this.fontColor,
        backgroundColor: this.backgroundColor,
      };
      this.$emit("updateSettings", newSettings);
      // Save new setting to local storage
      const settings = {
        fontSize: this.fontSize,
        fontColor: this.fontColor,
        backgroundColor: this.backgroundColor,
      };
      localStorage.setItem("chatbotSettings", JSON.stringify(settings));
    },
    
    // Method Reset settings to default values
    resetSettings() {
      this.fontSize = 16;
      this.fontColor = "#000000";
      this.backgroundColor = "#ffffff";
      this.updateSettings();
    }
  },
};
</script>

<style>
/* Styling for settings page */
.settings {
  padding: 20px;
  font-family: Arial, sans-serif;
}

/* Styling for setting values */
.settingsValues {
  margin-top: 50px;
}
h3 {
  display: block;
  font-size: var(--apply-font-size, 16px);
  margin-bottom: 10px;
  text-align: center;
}

/* Styling for font size selector */
.fontSizeSetting {
  display: flex;
  align-items: center;
  gap: 15px;
  justify-content: center;
  position: relative;
}
input[type="range"] {
  width: 80%;
  height: 12px;
  background: #d9d9d9;
  border-radius: 10px;
  appearance: none;
  outline: none;
  transition: background-color 0.3s ease;
}
.fontSizeValue {
  font-weight: bold;
  font-size: var(--apply-font-size, 16px);
}

/* Styling for font colour and background colour selector */
.colorSetting {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
}
input[type="color"] {
  width: 90px;
  height: 55px;
}
.colorDisplay {
  padding: 13px;
  background-color: #f5f5f5;
  border: 1px solid #ccc;
  border-radius: 5px;
  color: black;
}

/* Styling for reset button */
.resetButtonContainer {
  display: flex;
  justify-content: center;
  margin-top: 30px;
}
.resetButton {
  padding: 10px 20px;
  background-color: #e63946;
  border: none;
  border-radius: 5px;
  color: white;
  font-size: 20px;
  font-weight: bold;
}
.resetButton:hover {
  background-color: #d71e27;
}
</style>
