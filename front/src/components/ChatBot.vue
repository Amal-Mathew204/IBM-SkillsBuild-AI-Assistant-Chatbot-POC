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
                    {{ message.text }}
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
            messages: JSON.parse(localStorage.getItem("chatbotMessages")) || [
                { text: "Hi there! I am the IBM Skills Build Chatbot...", type: "received" },
            ],
            currentFontSize: JSON.parse(localStorage.getItem("chatbotSettings"))?.fontSize + "px" || this.fontSize,
            currentFontColor: JSON.parse(localStorage.getItem("chatbotSettings"))?.fontColor || this.fontColor,
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
    watch: {
        // Watches for any changes within the setting values 
        fontSize(newVal) {
            this.currentFontSize = newVal;
        },
        fontColor(newVal) {
            this.currentFontColor = newVal;
        },
    },
    methods: {
        //Method to send message
        sendMessage() {
            console.log("send message");
            if (!this.message.trim()) return; //helps stop sending empty messages
            this.messages.push({ text: this.message, type: "sent" });
            localStorage.setItem("chatbotMessages", JSON.stringify(this.messages));
            this.apiResponse(this.message)
            this.message = "";
            //Auto scrolls messags to the bottom so its in view
            this.$nextTick(() => {
                this.$refs.messagesContainer.scrollTop = this.$refs.messagesContainer.scrollHeight;
            });
        },
        //Method to reset chat
        resetChat() {
            localStorage.removeItem("chatbotMessages");
            this.messages = [{ text: "Hi there! I am the IBM Skills Build Chatbot...", type: "received" }];
        },
        async apiResponse(userQuery){
            try
                {
                  const response = await fetch (`/api/chatbot/${userQuery.replace("%20", "")}/${5}`,
                  {
                    method: "GET",
                  });
                  if (response.ok)
                  {
                    let data = await response.json();
                    console.log(data);
                    let text = "The following courses are recommended: "
                    let courses = data.courses
                    courses.forEach(element => {
                        text = text + element["title"] + "\n"
                    });
                    this.message = text
                    this.messages.push({ text: this.message, type: "received" });
                    localStorage.setItem("chatbotMessages", JSON.stringify(this.messages));
                    this.message = "";
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
    position: relative;
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
    margin: 45px 0px;
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
}
.message.sent .messageBox {
    background-color: #d9d9d9;
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
</style>