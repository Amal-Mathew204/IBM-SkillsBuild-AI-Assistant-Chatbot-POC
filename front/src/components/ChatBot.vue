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
                    <!-- Course reccomendation card -->
                    <div class="courseReccomendation" v-if="message.type === 'received'">
                        <h4>{{ message.text }}</h4>
                        <div v-if="message.courses !== undefined && message.courses.length !== 0">
                            <h4>{{ message.coursesReceived ? 'Recommended Courses:' : 'Similar Courses:' }}</h4>
                            <ul>
                                <li v-for="(course, i) in message.courses" :key="i">
                                    <div v-if="message.justifications !== undefined">
                                        <h4 >{{ message.justifications[i] }}</h4>
                                    </div>
                                    <a :href="message.courseURL[i]" target="_blank" class="courseLink">
                                        <strong>{{ course }}</strong>
                                    </a>
                                    <ul>
                                        <li>Type: {{ message.courseType[i] }}</li>
                                        <li>Completion Time: {{ message.timeCompletion[i] }}</li>
                                    </ul>
                                    <!-- See Similar Courses Button -->
                                    <button v-if= "message.coursesReceived !==undefined" @click="reverse_search(message.coursesReceived[i])" class="similarCoursesButton">See Similar Courses</button>
                                </li>
                            </ul>
                        </div>
                    </div>

                    <!--  if 'data science' is mentioned -->
                    <div class="dataScienceMessage" v-else-if="message.dataButton">
                        <h4>{{ message.text }}</h4>
                        <router-link to="/datascience">
                            <button class="dataButton">Data Science</button>
                        </router-link>
                    </div>
                    <div v-else>
                        {{ message.text }}
                    </div>
                </div>
                <div v-if="message.type === 'sent'">
                    <img src="@/assets/userIcon.png" class="messageIcon" />
                </div>
            </div>
        </div>
        <!-- Message input box -->
        <div class="messageInputBox">
            <input type="text" placeholder="Type Message Here" v-model="message" @keyup.enter="sendMessage" :style="settingStyle" />
            <button @click="sendMessage" class="sendButton" title="Send Message">
                <img src="@/assets/sendIcon.png" class="sendIcon" />
            </button>
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
        };
    },
    mounted() {
        this.fetchChat();
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
    methods: {
        //Method to send message
        sendMessage() {
            console.log("send message");
            if (!this.message.trim()) return; //helps stop sending empty messages
            this.messages.push({ text: this.message, type: "sent" });
            localStorage.setItem("chatbotMessages", JSON.stringify(this.messages));
            this.apiResponse(this.message);
            this.message = "";
            //Auto scrolls messags to the bottom so its in view
            this.$nextTick(() => {
                this.$refs.messagesContainer.scrollTop = this.$refs.messagesContainer.scrollHeight;
            });
        },
        //Method to reset chat
        // resetChat() {
        //     localStorage.removeItem("chatbotMessages");
        //     this.messages = [
        //         {text: "Welcome to the IBM Skills Build data science course assistant! To help you find the most relevant courses, I'd like to know about your educational background. Could you tell me about any degrees or qualifications you've completed?", type: "received" },
        //     ];
        //     localStorage.setItem("chatbotMessages", JSON.stringify(this.messages));
        // },
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
                        {text: "Welcome to the IBM Skills Build data science course assistant! To help you find the most relevant courses, I'd like to know about your educational background. Could you tell me about any degrees or qualifications you've completed?", type: "received" },
                    ];
                }
            } catch (error) {
                console.log(error);
            }
        },
        async fetchChat(){
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
                        if (message.type === "recieved"){
                            let courses = message.courses.map(course => course["title"]);
                            let timeCompletion = message.courses.map(course => course["learning_hours"]);
                            let courseType = message.courses.map(course => course["course_type"]);
                            let courseURL = message.courses.map(course => course["url"]);
                            let justifications = message.courses.map(course => course["justification"])
                            return {
                                text: message.text,
                                type: "received",
                                courses: courses,
                                timeCompletion: timeCompletion,
                                courseType: courseType,
                                courseURL: courseURL,
                                justifications: justifications,
                                coursesReceived: message.courses
                            }
                        }
                        else{
                            return message
                        }
                    });
                }
            } catch (error) {
                console.log(error);
            }
        },
        async apiResponse(userQuery) {
            try {
                const response = await fetch(`/api/chatbot/${userQuery.replace("%20", "")}/${5}`, {
                    method: "GET",
                });

                if (response.ok) {
                    let data = await response.json();
                    let courses = data.courses.map(course => course["title"]);
                    let timeCompletion = data.courses.map(course => course["learning_hours"]);
                    let courseType = data.courses.map(course => course["course_type"]);
                    let courseURL = data.courses.map(course => course["url"]);
                    let justifications = data.courses.map(course => course["justification"])
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

                    if (courses.some(course => course.toLowerCase().includes("data science"))) {
                        this.messages.push({
                            type: "received",
                            text: "Want to learn more about Data Science, Click the button below:",
                            dataButton: true,
                        });
                    }
                    this.message = "";
                    //Auto scrolls messags to the bottom so its in view
                    this.$nextTick(() => {
                        this.$refs.messagesContainer.scrollTop = this.$refs.messagesContainer.scrollHeight;
                    });
                }
            } catch (error) {
                console.log(error);
            }
        },

        //Gets cookies from page
        getCookie(cookieValueKey, cookies)
            {
                    const value = cookies.split('; ')
                                        .map(cookie => cookie.split('='))
                                        .find(([key]) => key === cookieValueKey);
                    
                return value ? decodeURIComponent(value[1]) : "";
            },

        async reverse_search (course_info){
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
                    console.log(data)
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
                    //Auto scrolls messags to the bottom so its in view
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

/* Router Message Container */
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

@media (max-width: 768px) {
    .messagesContainer {
        margin: 45px 0px;
    }
}
</style>
