import { Text, View, TextInput, TouchableOpacity, Image } from 'react-native';
import { styles } from './styles';


export function Home() {

  return (
    <View style= { styles.container }>
      <Text style={ styles.eventName }>
        MATCH
      </Text>

      <Text style={ styles.eventDate }>
        Shazam diretamente da Shopee
      </Text>
      <Text style={ styles.pressText }>
        Tap to Match
      </Text>
      <TouchableOpacity>
        <View style={ styles.shadowContainer }>
          <Image source={require('./../../foto.jpeg')} style={styles.image}/>
        </View>
      </TouchableOpacity>
      
      <Text style={ styles.joke }>
        Não é tinder, mas sempre temos um match para você!
      </Text>  
    </View>
  )
}