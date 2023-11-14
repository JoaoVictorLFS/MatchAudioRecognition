import { View, Text, TouchableOpacity } from 'react-native'
import { styles } from './styles'
type Props = {
    name: string
}

export function Participant({name}: Props) {
    return(
        <View style={ styles.container }>
            <Text style={ styles.name }>
                { name }
            </Text>

            <TouchableOpacity style={ styles.buttom }>
                <Text style={ styles.buttomText }>
                    -
                </Text>
            </TouchableOpacity>
        </View>
    )
};