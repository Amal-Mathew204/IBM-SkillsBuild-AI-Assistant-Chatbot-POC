<template>
    <div class="chatbotContainer">
        <!-- New Chat Button -->
        <div class="header">
            <button @click="resetChat" class="newChatButton" title="New Chat">
                <img src="@/assets/newChatIcon.png" class="newChatIcon" />
            </button>
        </div>
        <!-- Sent and Received messages -->
        <div class="messagesContainer" ref="messagesContainer">
            <div v-for="(message, index) in messages" :key="index" :class="['message', message.type]">
                <div v-if="message.type === 'received'">
                    <img src="@/assets/chatbotIcon.png" class="messageIcon" />
                </div>
                <div class="messageBox" :style="settingStyle">
                    <!--  Data Science message prompt -->
                    <div class="dataScienceMessage" v-if="message.type === 'received' && message.dataButton">
                        <h4>{{ message.text }}</h4>
                        <router-link to="/datascience">
                            <button class="dataButton" :style="`font-size: ${settingStyle.fontSize}`">Data Science</button>
                        </router-link>
                    </div>
                    <!-- Course recommendation card -->
                    <div class="courseReccomendation" v-else-if="message.type === 'received'">
                        <h4>{{ message.text }}</h4>
                        <div v-if="message.courses !== undefined && message.courses.length !== 0">
                            <h4>{{ message.coursesReceived ? 'Recommended Courses:' : 'Similar Courses:' }}</h4>
                            <ul>
                                <li v-for="(course, i) in message.courses" :key="i">
                                    <a :href="message.courseURL[i]" target="_blank" class="courseLink">
                                        <h4 class ="courseTitle">{{ course }}</h4>
                                    </a>
                                    <div v-if="message.justifications !== undefined">
                                        <h4 :style="settingStyle">{{ message.justifications[i] }}</h4>
                                    </div>
                                    <ul>
                                        <li>Type: {{ message.courseType[i] }}</li>
                                        <li>Completion Time: {{ message.timeCompletion[i] }}</li>
                                    </ul>
                                    <!-- See Similar Courses Button -->
                                    <button v-if="message.coursesReceived !== undefined" @click="reverse_search(message.coursesReceived[i])" class="similarCoursesButton" :style="`font-size: ${settingStyle.fontSize}`" >See Similar Courses</button>
                                </li>
                            </ul>
                        </div>
                    </div>
                    <div v-else>
                        {{ message.text }}
                    </div>
                </div>
                <div v-if="message.type === 'sent'">
                    <img src="@/assets/userIcon.png" class="messageIcon" />
                </div>
            </div>
                <!-- Typing indicator for chatbot -->
                <div v-if="loading" class="typingIndicator">
                    <img src="@/assets/chatbotIcon.png" class="messageIcon" />
                    <span class="typingText" :style="`font-size: ${settingStyle.fontSize};`">Chatbot is typing</span>
                    <div class="typingAnimation">
                        <span class="typingDot" :style="`width: calc(${settingStyle.fontSize} - 7px); height: calc(${settingStyle.fontSize} - 7px);`"></span>
                        <span class="typingDot" :style="`width: calc(${settingStyle.fontSize} - 7px); height: calc(${settingStyle.fontSize} - 7px);`"></span>
                        <span class="typingDot" :style="`width: calc(${settingStyle.fontSize} - 7px); height: calc(${settingStyle.fontSize} - 7px);`"></span>
                    </div>
                </div>
            <div>
                <!-- Message input box -->
                <div class="messageInputBox">
                    <input type="text" v-model="message" @keyup.enter="sendMessage" :style="settingStyle" :disabled="loading"  :placeholder="loading ? 'Please wait until the chatbot has finished thinking' : 'Type Message Here'" />
                    <button @click="sendMessage" class="sendButton" title="Send Message" :disabled="loading">
                        <img src="@/assets/sendIcon.png" class="sendIcon" />
                    </button>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    name: "ChatBot",
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
        // Defines settings values and messages
        return {
            message: "",
            messages: [],
            currentFontSize: JSON.parse(localStorage.getItem("chatbotSettings"))?.fontSize + "px" || this.fontSize,
            currentFontColor: JSON.parse(localStorage.getItem("chatbotSettings"))?.fontColor || this.fontColor,
            loading: false, // chatbot is typing = false so animation does not show
        };
    },
    mounted() {
        this.fetchChat();
    },
    computed: {
        // Creates dynamic CSS object
        settingStyle() {
            return {
                fontSize: this.currentFontSize,
                color: this.currentFontColor,
            };
        },
    },
    methods: {
        // Method to send message
        sendMessage() {
            console.log("send message");
            if (!this.message.trim()) return; // helps stop sending empty messages
            this.messages.push({ text: this.message, type: "sent" });
            localStorage.setItem("chatbotMessages", JSON.stringify(this.messages));
            this.apiResponse(this.message);
            this.message = "";
            // Auto scrolls messages to the bottom so it's in view
            this.$nextTick(() => {
                this.$refs.messagesContainer.scrollTop = this.$refs.messagesContainer.scrollHeight;
            });
        },

        // Method to reset converstaion history to default
        async resetChat() {
            try {
                const csrfToken = this.getCookie("csrftoken", document.cookie);
                const response = await fetch("/api/resetchat/", {
                    method: 'PUT',
                    credentials: "same-origin",
                    mode: 'cors',
                    headers: {
                        'Content-Type': 'application/json',
                        'Cookie': document.cookie,
                        'x-csrftoken': csrfToken,
                    }
                });
                if (response.ok) {
                    this.messages = [
                        { text: "Welcome to the IBM Skills Build data science course assistant! To help you find the most relevant courses, I'd like to know about your educational background. Could you tell me about any degrees or qualifications you've completed?", type: "received" },
                    ];
                }
            } catch (error) {
                console.log(error);
            }
        },

        // Method to fetch chat after a refresh
        async fetchChat() {
            try {
                const response = await fetch("/api/fetchchat/", {
                    method: 'GET',
                    headers: {
                        'Content-Type': 'application/json',
                    }
                });
                if (response.ok) {
                    let content = await response.json();
                    this.messages = content["chat_history"].map(message => {
                        if (message.type === "recieved") {
                            let courses = message.courses.map(course => course["title"]);
                            let timeCompletion = message.courses.map(course => course["learning_hours"]);
                            let courseType = message.courses.map(course => course["course_type"]);
                            let courseURL = message.courses.map(course => course["url"]);
                            let justifications = message.courses.map(course => course["justification"]);
                            return {
                                text: message.text,
                                type: "received",
                                courses: courses,
                                timeCompletion: timeCompletion,
                                courseType: courseType,
                                courseURL: courseURL,
                                justifications: justifications,
                                coursesReceived: message.courses
                            };
                        }
                        else {
                            return message;
                        }
                    });
                }
            } catch (error) {
                console.log(error);
            }
        },

        //Method for fetching api response 
        async apiResponse(userQuery) {
            try {
                // typing indiactor set to true
                this.loading = true;
                const response = await fetch(`/api/chatbot/${userQuery.replace("%20", "")}/${5}`, {
                    method: "GET",
                });

                if (response.ok) {
                    let data = await response.json();
                    let courses = data.courses.map(course => course["title"]);
                    let timeCompletion = data.courses.map(course => course["learning_hours"]);
                    let courseType = data.courses.map(course => course["course_type"]);
                    let courseURL = data.courses.map(course => course["url"]);
                    let justifications = data.courses.map(course => course["justification"]);
                    let responseMessage = {
                        text: data["text_response"],
                        type: "received",
                        courses: courses,
                        timeCompletion: timeCompletion,
                        courseType: courseType,
                        courseURL: courseURL,
                        justifications: justifications,
                        coursesReceived: data.courses
                    };
                    this.messages.push(responseMessage);

                    //If course mentions data science
                    if (courses.some(course => course.toLowerCase().includes("data science"))) {
                        this.messages.push({
                            type: "received",
                            text: "Want to learn more about Data Science, Click the button below:",
                            dataButton: true,
                        });
                    }

                    // Hide typing indicator and text input is blank 
                    this.loading = false;
                    this.message = "";

                    // Auto scrolls messages to the bottom so it's in view
                    this.$nextTick(() => {
                        this.$refs.messagesContainer.scrollTop = this.$refs.messagesContainer.scrollHeight;
                    });
                }
            } catch (error) {
                console.log(error);
                this.loading = false; // Hide loading indicator on error
            }
        },

        // Gets cookies from the page
        getCookie(cookieValueKey, cookies) {
            const value = cookies.split('; ')
                .map(cookie => cookie.split('='))
                .find(([key]) => key === cookieValueKey);

            return value ? decodeURIComponent(value[1]) : "";
        },

        async reverse_search(course_info) {
            try {
                course_info = JSON.parse(JSON.stringify(course_info));
                const csrfToken = this.getCookie("csrftoken", document.cookie);
                const response = await fetch("/api/similarcourses/", {
                    method: 'POST',
                    credentials: "same-origin",
                    mode: 'cors',
                    headers: {
                        'Content-Type': 'application/json',
                        'Cookie': document.cookie,
                        'x-csrftoken': csrfToken,
                    },
                    body: JSON.stringify({
                        "course": JSON.parse(JSON.stringify(course_info)),
                    })
                });

                if (response.ok) {
                    let data = await response.json();
                    let courses = data.similar_courses.map(course => course["title"]);
                    let timeCompletion = data.similar_courses.map(course => course["learning_hours"]);
                    let courseType = data.similar_courses.map(course => course["course_type"]);
                    let courseURL = data.similar_courses.map(course => course["url"]);
                    let responseMessage = {
                        type: "received",
                        courses: courses,
                        timeCompletion: timeCompletion,
                        courseType: courseType,
                        courseURL: courseURL,
                    };
                    this.messages.push(responseMessage);
                    console.log(data);
                    this.message = "";
                    // Auto scrolls messages to the bottom so it's in view
                    this.$nextTick(() => {
                        this.$refs.messagesContainer.scrollTop = this.$refs.messagesContainer.scrollHeight;
                    });
                }
            } catch (error) {
                console.log(error);
            }
        }
    },
};
</script>

<style>
/* Styling for chatbot page */
.chatbotContainer {
    display: flex;
    flex-direction: column;
    justify-content: flex-end;
    align-items: center;
    width: 100%;
    height: 80%;
}

/* Styling for new chat button */
.header {
    position: fixed;
    top: 10px;
    right: 10px;
}
.newChatButton {
    background: transparent;
    border: none;
}
.newChatIcon {
    height: 50px;
    width: 50px;
    transition: transform 0.5s ease-in-out;
}
.newChatButton:hover .newChatIcon {
    transform: scale(1.3);
}

/* Styling for chatbot and user messages */
.messagesContainer {
    display: flex;
    width: 95%;
    flex-direction: column;
    margin-top: 60px;
    overflow-y: auto;
    flex-grow: 1;
}
.message {
    display: flex;
    align-items: center;
    max-width: 100%;
}
.message.sent {
    justify-content: flex-end;
}

.message.received {
    justify-content: flex-start;
    margin-bottom: 10px;
}
.messageIcon {
    width: 100px;
    height: 100px;
}
.messageBox {
    padding: 10px 15px;
    background-color: #d9d9d9;
    max-width: 100%;
    border-radius: 15px;
    box-shadow: 0px 3px 6px rgba(0, 0, 0, 0.1);
}
.message.sent .messageBox {
    background-color: #7fc0fc;
}

/* course reccomendation Styling */
.courseReccomendation {
    background: #ffffff;
    padding: 25px;
    border-radius: 12px;
    border-left: 6px solid #0083ff;
    margin-top: 10px;
    padding-right: 20px;
}
.courseReccomendation h4 {
    margin-bottom: 10px;
    color: #007bff;
    font-weight: bold;
    font-size: inherit;
}
.courseReccomendation ul {
    list-style: none;
    padding: 0;
    margin: 0;
}
.courseReccomendation li {
    background: #f8f9fa;
    padding: 12px;
    border-radius: 8px;
    margin-bottom: 8px;
}
.courseReccomendation li strong {
    color: #343a40;
    font-size: inherit;
}
.courseLink {
    color: #0083ff;
    text-decoration: none;
    font-weight: bold;
}
.courseLink:hover {
    text-decoration: underline;
}
.courseTitle{
    color: #007bff;
    font-weight: bolder;
}
.courseReccomendation ul ul {
    margin-top: 5px;
    padding-left: 15px;
}
.courseReccomendation ul ul li {
    font-size: inherit;
}

/* Styling for message input box */
.messageInputBox {
    background-color: #d9d9d9;
    display: flex;
    align-items: center;
    width: 70%;
    position: fixed;
    bottom: 20px;
    border-radius: 25px;
    padding: 15px 10px;
    margin-bottom: 1.2vh;
    box-shadow: 0px 3px 6px rgba(0, 0, 0, 0.1);
}
.messageInputBox input {
    flex-grow: 1;
    border: none;
    outline: none;
    background: transparent;
    font-size: 16px;
    padding: 5px;
}
.messageInputBox input::placeholder {
    color: grey;
    font-weight: bold;
}
.messageInputBox .sendButton {
    background: transparent;
    border: none;
    margin-left: 10px;
}
.sendButton {
    border: none;
    background: transparent;
    margin-left: 10px;
}
.sendButton .sendIcon {
    height: 30px;
    width: 30px;
    transition: transform 0.3s ease-in-out;
}
.sendButton:hover .sendIcon {
    transform: scale(1.3);
}

/* Data Science prompt styling*/
.dataScienceMessage {
    background: #f9f9f9;
    padding: 12px;
    border-radius: 10px;
    box-shadow: 0px 3px 6px rgba(0, 0, 0, 0.1);
    margin: 5px;
    border-left: 6px solid #007bff;
}

/* Button Styling */
.dataButton, .similarCoursesButton {
    display: block;
    margin-top: 10px;
    background: linear-gradient( #007bff, #0056b3);
    color: #ffffff;
    border: none;
    padding: 10px 14px;
    font-size: 15px;
    font-weight: bold;
    border-radius: 6px;
    cursor: pointer;
    text-align: center;
    transition: all 0.2s ease-in-out;
    text-decoration: none;
}
.dataButton:hover, .similarCoursesButton:hover {
    background: linear-gradient(#0056b3, #004494);
    transform: scale(1.05);
}

/* Styling for the typing indicator */
.typingIndicator {
    display: flex;
    align-items: center;
    justify-content: flex-start;
    margin-top: 10px;
}
.typingText {
    color: #007bff;
    font-size: 16px;
    margin-right: 10px;
}
.typingAnimation {
    display: flex;
    align-items: center;
}
.typingDot {
    width: 10px;
    height: 10px;
    margin: 0 3px;
    background-color: #007bff;
    border-radius: 50%;
    animation: typing 1.5s infinite ease-in-out;
}
.typingDot:nth-child(1) {
    animation-delay: 0s;
}
.typingDot:nth-child(2) {
    animation-delay: 0.3s;
}
.typingDot:nth-child(3) {
    animation-delay: 0.6s;
}
@keyframes typing {
    0% {
        opacity: 0;
    }
    50% {
        opacity: 1;
    }
    100% {
        opacity: 0;
    }
}

/* Mobile CSS */
@media (max-width: 768px) {
    .messagesContainer {
        margin: 45px 0px;
    }
}
</style>
