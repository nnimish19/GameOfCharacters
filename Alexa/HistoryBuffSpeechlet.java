package historybuff;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.net.URL;
import java.nio.charset.Charset;
import java.text.DateFormat;
import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Calendar;
import java.util.Collections;
import java.util.Date;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

import org.apache.commons.io.IOUtils;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import com.amazon.speech.slu.Intent;
import com.amazon.speech.slu.Slot;
import com.amazon.speech.speechlet.IntentRequest;
import com.amazon.speech.speechlet.LaunchRequest;
import com.amazon.speech.speechlet.Session;
import com.amazon.speech.speechlet.SessionEndedRequest;
import com.amazon.speech.speechlet.SessionStartedRequest;
import com.amazon.speech.speechlet.Speechlet;
import com.amazon.speech.speechlet.SpeechletException;
import com.amazon.speech.speechlet.SpeechletResponse;
import com.amazon.speech.ui.OutputSpeech;
import com.amazon.speech.ui.PlainTextOutputSpeech;
import com.amazon.speech.ui.SsmlOutputSpeech;
import com.amazon.speech.ui.Reprompt;
import com.amazon.speech.ui.SimpleCard;


public class HistoryBuffSpeechlet implements Speechlet {
    private static final Logger log = LoggerFactory.getLogger(HistoryBuffSpeechlet.class);

    @Override
	public SpeechletResponse onLaunch(LaunchRequest request, Session session) throws SpeechletException {
		log.info("onLaunch requestId={}, sessionId={}", request.getRequestId(),
                session.getSessionId());
		
		return greeting();
	}
    
	@Override
	public SpeechletResponse onIntent(IntentRequest request, Session session) throws SpeechletException {
		log.info("onIntent requestId={}, sessionId={}", request.getRequestId(),
                session.getSessionId());

	    Intent intent = request.getIntent();
	    String intentName = (intent != null) ? intent.getName() : null;
	    if ("WhoIsX".equals(intentName)) {
	        return getWhoIsX(intent, session);
	    } else if ("RelationOfXandY".equals(intentName)) {
	        return getRelationOfXandY(intent, session);
	    } else if ("AMAZON.StopIntent".equals(intentName)) {
            PlainTextOutputSpeech outputSpeech = new PlainTextOutputSpeech();
            outputSpeech.setText("Goodbye");

            return SpeechletResponse.newTellResponse(outputSpeech);
        } else if ("AMAZON.CancelIntent".equals(intentName)) {
            PlainTextOutputSpeech outputSpeech = new PlainTextOutputSpeech();
            outputSpeech.setText("Goodbye");
        }
	    else {
            throw new SpeechletException("Invalid Intent");
        }
	    return null;
    }
	
	@Override
	public void onSessionEnded(SessionEndedRequest arg0, Session arg1) throws SpeechletException {
		// TODO Auto-generated method stub
		
	}

	@Override
	public void onSessionStarted(SessionStartedRequest arg0, Session arg1) throws SpeechletException {
		// TODO Auto-generated method stub
		
	}
	
	SpeechletResponse greeting(){
		PlainTextOutputSpeech pt = new PlainTextOutputSpeech();
		String greetingMessage = "Hello, Welcome to Game of Characters."+
				" You can ask the following questions."+
				" 1. Who is X? where X is any character."+
				" 2. What is the relation of X and Y? where X and Y both are different characters.";
		pt.setText(greetingMessage);
		
		SimpleCard sd = new SimpleCard();
		sd.setTitle("GOT");
		sd.setContent("Hello, Welcome to Game of Characters");
		
		PlainTextOutputSpeech pt1 = new PlainTextOutputSpeech();
		String noreplyMessage = "You seem confused."+
				" Here are the instructions again."+
				" You can ask the following questions."+
				" 1. Who is X? where X is any character."+
				" 2. What is the relation of X and Y? where X and Y both are different characters.";
				
		pt1.setText(noreplyMessage);
		
		Reprompt rpt = new Reprompt();
		rpt.setOutputSpeech(pt1);
		
		return SpeechletResponse.newAskResponse(pt, rpt, sd);
	}

	private SpeechletResponse getWhoIsX(Intent intent, Session session) {
		PlainTextOutputSpeech pt = new PlainTextOutputSpeech();
		Slot name = intent.getSlot("Character");	//Slot name
		String val = name.getValue();				//Slot value
		
		val = val.toLowerCase();
		
		if (val.equals("john")){	//Here there will be a list of characters
			pt.setText("Loop1");	//Here we will return the answer for corresponding character
		}
		
		SimpleCard sd = new SimpleCard();
		sd.setTitle("WhoIsX");
		sd.setContent("CharacterX" + " " + val);
		
		return SpeechletResponse.newTellResponse(pt, sd);
		}

	
	private SpeechletResponse getRelationOfXandY(Intent intent, Session session) {
		PlainTextOutputSpeech pt = new PlainTextOutputSpeech();
		Slot name1 = intent.getSlot("CharacterX"); 
		Slot name2 = intent.getSlot("CharacterY"); 
		String val1 = name1.getValue();
		String val2 = name2.getValue();
		
		String ans = "qqqqqqqqq";
		pt.setText(val1 + val2);
		
		SimpleCard sd = new SimpleCard();
		sd.setTitle("RelationOfXandY");
		sd.setContent("CharacterX and CharacterY"+" " +val1 +" " +val2);
		
		return SpeechletResponse.newTellResponse(pt, sd);
	}
}
