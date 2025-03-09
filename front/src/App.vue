<template>
  <div class="app" :style="appSettings">
    <!-- Nav Bar -->
    <nav class="navBar" :class="{ open: isnavBarOpen }">
      <img src="@/assets/logo.png" class="logo" />
      <ul>
        <li>
          <router-link to="/" class="navButtons" :class="{ active: activeLink === 'ChatBot' }" @click="setActive('ChatBot')">
            ChatBot
          </router-link>
        </li>
        <li>
          <a href="https://skillsbuild.org/learners" target = "_blank" rel="noopener noreferrer"  class="navButtons">
            Learners
          </a>
        </li>
        <li>
          <a href="https://skillsbuild.org/educators" target = "_blank" rel="noopener noreferrer"  class="navButtons">
            Educators
          </a>
        </li>
        <li>
          <a href="https://skillsbuild.org/organizations" target = "_blank" rel="noopener noreferrer" class="navButtons">
            Organizations
          </a>
        </li>
        <li>
          <a href="https://skillsbuild.org/events" target = "_blank" rel="noopener noreferrer" class="navButtons">
            Events
          </a>
        </li>
        <li>
          <router-link to="/settings" class="navButtons" :class="{ active: activeLink === 'settings' }" @click="setActive('settings')">
            Settings
          </router-link>
        </li>
      </ul>
    </nav>
    <!-- Nav Bar for smaller screen size-->
    <div class="navBarSmall" @click="shownavBar">
      <button class="navBarSmallButton">
        <img src="@/assets/menuIcon.png" class="navBarSmallIcon" title="Open Nav Bar" />
      </button>
    </div>
    <!-- Main content-->
    <div class="mainContent">
      <router-view :font-size="appSettings.fontSize" :font-color="appSettings.color" @updateSettings="updateSettings" />
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      activeLink: "ChatBot",
      appSettings: {
        fontSize: "16px",
        color: "#000000",
        backgroundColor: "#ffffff",
      },
      isnavBarOpen: false,
    };
  },
  mounted() {
    // Fetch saved settings and active link as before
    const savedSettings = JSON.parse(localStorage.getItem("chatbotSettings"));
    if (savedSettings) {
      this.appSettings.fontSize = savedSettings.fontSize;
      this.appSettings.color = savedSettings.fontColor;
      this.appSettings.backgroundColor = savedSettings.backgroundColor;
    }
    const savedActiveLink = localStorage.getItem("activeLink");
    if (savedActiveLink) {
      this.activeLink = savedActiveLink;
    }
    this.applySettings(this.appSettings);
  },
  methods: {
    // Set state (Show or hide) nav bar in smaller screens
    shownavBar() {
      this.isnavBarOpen = !this.isnavBarOpen;
      const navBar = document.querySelector('.navBar');
      if (this.isnavBarOpen) {
        navBar.classList.add('open');
      } else {
        navBar.classList.remove('open');
      }
    },
    setActive(link) {
      this.activeLink = link;
      localStorage.setItem("activeLink", link);
    },
    updateSettings(newSettings) {
      this.appSettings = newSettings;
      this.applySettings(newSettings);
      localStorage.setItem("chatbotSettings", JSON.stringify({
        fontSize: newSettings.fontSize,
        fontColor: newSettings.color,
        backgroundColor: newSettings.backgroundColor,
      }));
    },
    applySettings(settings) {
      document.documentElement.style.setProperty("--apply-font-size", settings.fontSize);
      document.documentElement.style.setProperty("--apply-color", settings.color);
      document.documentElement.style.setProperty("--apply-background-color", settings.backgroundColor);
    },
  },
};
</script>

<style>
/* Styling for entire app */
.app {
  display: flex;
  height: 100vh;
  font-family: Arial, sans-serif;
  margin: 0;
  padding: 0;
  width: 100%;
  height: 100%;
  transition: all 0.5s ease;
  position: fixed;
  top: 0;
  left: 0;
  bottom: 0;
}

/* Styling for nav bar */
.navBar {
  background-color: #2D2A2A;
  width: 290px;
  height: 100vh;
  padding: 20px 10px;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  position: fixed;
  top: 0;
  left: 0;
  bottom: 0;
  transition: transform 0.3s ease-in-out;
  z-index: 1; 
}
.navBar .logo {
  width: 100px;
  margin-top: 10px;
  margin-bottom: 20px;
  margin-left: auto;
  margin-right: auto;
  display: block;
}
.navBar ul {
  list-style: none;
  padding: 0;
  width: 100%;
  text-align: center;
}
.navBar .navButtons {
  display: block;
  color: white;
  text-decoration: none;
  margin-top: 20px;
  font-size: 20px;
  padding: 8px 12px;
  font-weight: bold;
  transition: background-color 0.5s ease;
}
.navBar .navButtons:hover {
  background-color: #333;
}
.navBar .navButtons.active {
  color: white;
  background-color: #0083ff;
}

/* NavBar menu button for mobile */
.navBarSmall {
  display: none;
  font-size: 30px;
  position: absolute;
  top: 20px;
  left: 20px;
  z-index: 2;
}
.navBarSmallButton {
  background-color: transparent;
  border: none;
  padding: 10px;
}
.navBarSmallIcon {
  width: 35px; 
  height: 35px;
  transition: transform 0.5s ease-in-out;
  display: block;
}
.navBarSmallButton:hover .navBarSmallIcon {
    transform: scale(1.3);
}

/* Styling for content */
.mainContent {
  padding: 20px;
  width: 100%;
  height: 100vh;
  margin-left: 290px;
  overflow-y: auto;
}

/* Responsive Design for Mobile Screens */
@media (max-width: 768px) {
  .navBar {
    width: 100%;
    height: 100%;
    transform: translateX(-100%); 
  }
  .navBar.open {
    transform: translateX(0); 
  }
  .mainContent {
    margin-top: 50px;
    margin-left: 0;
    padding: 10px;
    width: 100%; 
  }
  .navBarSmall {
    display: block;
  }
}
</style>
