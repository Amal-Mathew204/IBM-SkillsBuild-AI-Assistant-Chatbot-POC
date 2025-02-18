<template>
    <div class="dataScience" :style="settings">
        <!-- Back Button -->
        <div class="backButton">
            <router-link to="/">
                <button>
                <img src="@/assets/backIcon.png" alt="Back" class="arrowIcon">
                </button>
            </router-link>
        </div>
        <!-- Data Science information -->
        <div class="content">
            <div class="badge">
                <img src="@/assets/dataScienceIcon.png" alt="Badege Icon" class="badgeIcon"/>
                <h2>IBM SkillsBuild: Getting Started with Data Science</h2>
            </div>
            <div class="information" :style="settingStyle">
                <h3>What is Data Science?</h3>
                <p>
                    Data Science represents the use of extracting raw data by using various algorithms, programming and different machine learning 
                    tools. It involves multiple stages such as extracting, cleaning and processing large quantity of data to gain meaningful insights. By using 
                    these insights, they can be applied to improve business strategies, autonomation and streamlining tasks. Ultimately, data science revolves around
                    gathering data to make informed decisions.

                </p>
                <p></p>
                <p>
                    To learn more about data science, <a href="https://youtu.be/RBSUwFGa6Fk?si=tx1XqkSJpBd85_jZ">click this link</a> to watch a short video on "What is Data Science?"
                </p>
                <h3>Use cases for Data Science</h3>
                <p>
                    There are multiple use cases for data science from helping to train AI models to predicting consumer habits to optimising navigation routes. The possibilities are endless.
                    Here at IBM we utilise data science to tackle many problems across multiple different industries. We are proud to have worked with companies such as Shanghai Changjiang Science and Technology Development
                    to develop an <a href="https://www.ibm.com/case-studies/shanghai-changjiang-science-and-technology-development-co-ltd">AI-based medical assessment platform </a> to predict the success rate of different treatments for patients
                    based on their medical records. As more industries embrace digital transformation, the possible use cases for data science are limitless.
                </p>
                <h3>Benefits of completing the course</h3>
                <p>
                    Here at SkillsBuild we offer many data science courses to help people with different levels of technical proficiency. The IBM SkillsBuild: Getting Started with Data Science is a great course for beginners
                    trying to introduce themselves to the world of Data Science. Upon completion of the course, you will receive an IBM SkillsBuild badge which can be used to showcase your new skills to employers and workers.
                </p>
                <p></p>
                <p>
                    To find out more about the Data Science courses we offer, <a href="https://skillsbuild.org/students/course-catalog/data-science">click here</a> to visit our Data Science SkillsBuild page.
                </p>
            </div>
        </div>
    </div>
  </template>
  
<script>
export default {
    name: "DataScience",
    //Props to receive settings from app.vue
    //If no props value is given default value is used
    props: {
        fontSize: {
            type: String, 
            default: "16px",
        },
        fontColor: {
            type: String,
            default: "#000000",
        },
    },
    data() {
        // Defines settings values
        return {
            currentFontSize: this.fontSize,
            currentFontColor: this.fontColor,
        };
    },
    computed: {
        //Creates dynnamic css object
        settingStyle() {
            return {
            fontSize: this.currentFontSize,
            color: this.currentFontColor,
            };
        },
    },
    mounted() {
      //Retrieves settings from local sorafe
      const savedSettings = JSON.parse(localStorage.getItem("chatbotSettings"));
      if (savedSettings) {
        //If setting is found value is updated
        this.currentFontSize = savedSettings.fontSize + "px"; 
        this.currentFontColor = savedSettings.fontColor;
      }
    },
    watch: {
      // Watches for any changes within the setting values 
      fontSize(newVal) {
        this.currentFontSize = newVal; 
      },
      fontColor(newVal) {
        this.currentFontColor = newVal;
      },
    },
};
</script>
  
<style>
/* Styling for data science page */
.dataScience {
    display: flex;
    flex-direction: column;
    padding: 20px;
}

/* Styling for back button */
button {
    background: none; 
    border: none; 
    padding: 0;
    outline: none;
    display: flex;
    justify-content: center;
    align-items: center;
}
.arrowIcon {
    width: 74px;
    height: 64px;
    transition: transform 0.3s ease;
}

.backButton button:hover .arrowIcon {
    transform: scale(1.3);
}

/* Styling for information */
.content {
    display: flex;
    flex-direction: column;
    background-color: var(--apply-background-color, #fff);
    padding: 20px;
}
.badge {
    text-align: center;
}
.badgeIcon {
    width: 200px;
    height: auto;
    margin-bottom: 20px;
}
a:link {
  color: #0083ff;
  font-weight: bold;
  text-decoration: none;
}
a:visited {
  color: #0083ff;
}
a:hover {
  color: #528fc8;
}
.information h3 {
    font-size: var(--apply-font-size, 16px);
    color: var(--apply-color, #000);
    align-items: center;
}
.information p {
    text-align: center;
    font-size: calc(var(--apply-font-size, 16px) * 0.9);
    color: var(--apply-color, #000);
}
</style>