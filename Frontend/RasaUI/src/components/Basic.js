import './chatBot.css';
import react, { useEffect, useState } from 'react';
import {IoMdSend}  from 'react-icons/io';
import {BiBot,BiUser} from 'react-icons/bi';



function Basic(){
    const [chat,setChat] = useState([]);
    const [inputMessage,setInputMessage] = useState('');
    const [botTyping,setbotTyping] = useState(false);
    const [chatmodelrnn,setChatrnn] = useState('');

    
   useEffect(()=>{
   
        console.log("called");
        const objDiv = document.getElementById('messageArea');
        objDiv.scrollTop = objDiv.scrollHeight;
        
    
    },[chat])

    


    const handleSubmit=(evt)=>{
        evt.preventDefault();
        const name = "Abhishek";
        const request_temp = {sender : "user", sender_id : name , msg : inputMessage};
        
        if(inputMessage !== ""){
            
            setChat(chat => [...chat, request_temp]);
            setbotTyping(true);
            setInputMessage('');
            setChatrnn('');
            rnnAPI(name,inputMessage);
        
            rasaAPI(name,inputMessage);
        }
        else{
            window.alert("Please enter valid message");
        }
        
    }

    const rnnAPI = async function handleClick1(name,msg) {
    
        //chatData.push({sender : "user", sender_id : name, msg : msg});
        
          await fetch('/', {
            method: 'POST',
            headers: {
              'Content-Type':'application/json'
            },
            
            body: JSON.stringify({ "sender": name, "message": msg }),
    
          })
        .then(response => response.json())
        .then((response) => {
            if(response){
                console.log(response)
                const temp = response[0];
                console.log(temp)
                const recipient_id = temp["recipient_id"];
                const recipient_msg = temp["text"];        


                const response_rnn = {sender: "bot",recipient_id : recipient_id,msg: recipient_msg};
                // setbotTyping(false);
                
                setChatrnn(recipient_msg);
               // scrollBottom();
               console.log(chatmodelrnn)
               console.log(recipient_msg)

            }
        }) 
    }



    const rasaAPI = async function handleClick(name,msg) {


          await fetch('http://localhost:5005/webhooks/rest/webhook', {
            method: 'POST',
            headers: {
              'Accept': 'application/json',
              'Content-Type': 'application/json',
              'charset':'UTF-8',
            },
            credentials: "same-origin",
            body: JSON.stringify({ "sender": name, "message": msg }),
        })
        .then(response => response.json())
        .then((response) => {
            console.log(response)
            if(response){
            
                const temp = response[0];
           
                const recipient_id = temp["recipient_id"];
                const recipient_msg = temp["text"];        


                const response_temp = {sender: "bot",recipient_id : recipient_id,msg: recipient_msg};
                setbotTyping(false);
                if(chatmodelrnn.length>recipient_msg.length){
                    const response_temp = {sender: "bot",recipient_id : recipient_id,msg: chatmodelrnn}
                    setChat(chat => [...chat, response_temp]);
                }
                else{
                    setChat(chat => [...chat, response_temp]);
                }
                // setChat(chat => [...chat, response_temp]);
                
               // scrollBottom();

            }
        }) 
    }

    console.log(chat);

    const stylecard = {
        maxWidth : '35rem',
        border: '1px solid black',
        paddingLeft: '0px',
        paddingRight: '0px',
        borderRadius: '30px',
        boxShadow: '0 16px 20px 0 rgba(0,0,0,0.4)'

    }
    const styleHeader = {
        height: '5.5rem',
        borderBottom : '1px solid black',
        borderRadius: '30px 30px 0px 0px',
        backgroundColor: '#8012c4',

    }
    const styleFooter = {
        //maxWidth : '32rem',
        borderTop : '1px solid black',
        borderRadius: '0px 0px 30px 30px',
        backgroundColor: '#8012c4',
        
        
    }
    const styleBody = {
        paddingTop : '10px',
        height: '28rem',
        overflowY: 'a',
        overflowX: 'hidden',
        
    }

    return (
      <div>
        {/* <button onClick={()=>rasaAPI("shreyas","hi")}>Try this</button> */}
        

        <div className="container">
        <div className="row justify-content-center">
            
                <div className="card" style={stylecard}>
                    <div className="cardHeader text-white" style={styleHeader}>
                        <h1 style={{marginTop:'10px'}}>Valley Chat</h1>
                        {botTyping ? <h6>Bot Typing....</h6> : null}
                        
                        
                        
                    </div>
                    <div className="cardBody" id="messageArea" style={styleBody}>
                        
                        <div className="row msgarea">
                            {chat.map((user,key) => (
                                <div key={key}>
                                    {user.sender==='bot' ?
                                        (
                                            
                                            <div className= 'msgalignstart'>
                                                <BiBot className="botIcon"  /><h5 className="botmsg">{user.msg}</h5>
                                            </div>
                                        
                                        )

                                        :(
                                            <div className= 'msgalignend'>
                                                <h5 className="usermsg">{user.msg}</h5><BiUser className="userIcon" />
                                            </div>
                                        )
                                    }
                                </div>
                            ))}
                            
                        </div>
                
                    </div>
                    <div className="cardFooter text-white" style={styleFooter}>
                        <div className="row">
                            <form style={{display: 'flex'}} onSubmit={handleSubmit}>
                                <div className="col-10" style={{paddingRight:'0px'}}>
                                    <input onChange={e => setInputMessage(e.target.value)} value={inputMessage} type="text" className="msginp"></input>
                                </div>
                                <div className="col-2 cola">
                                    <button type="submit" className="circleBtn" ><IoMdSend className="sendBtn" /></button>
                                </div>
                            </form>
                        </div>
                    </div>
                </div>
            
        </div>
        </div>

      </div>
    );
}
  
export default Basic;
