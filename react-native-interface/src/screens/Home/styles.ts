import { StyleSheet } from 'react-native';

export const styles = StyleSheet.create({
    container: {
      flex: 1,
      backgroundColor: '#111e3f',
      padding: 24,
      alignItems: 'center',
    },
    eventName: {
      color: '#FFFFFF',
      fontSize: 48,
      fontWeight: 'bold',
      marginTop: 60
    },
    eventDate: {
      color: '#d7e0e7',
      fontSize: 16
    },
    input: {
        height: 56,
        backgroundColor: '#FFFFFF',
        borderRadius: 5,
        color: '#6B6B6B',
        padding: 16,
        fontSize: 16,
        flex: 1,
        marginRight: 12
    },
    buttomText: {
        color: '#FFFFFF',
        fontSize: 20
    },
    buttom: {
        width: 56,
        height: 56,
        borderRadius: 5,
        backgroundColor: '#31CF67',
        alignItems: 'center',
        justifyContent: 'center'
    },
    form: {
      width: '100%',
      flexDirection: 'row',
      marginTop: 36,
      marginBottom: 42
    },
    image: {
      marginTop: '25%',
      width: 200,
      height: 195,
      borderRadius: 100, 
    },
    shadowContainer: {
      shadowColor:"#FFFFFF",
      shadowOffset:{
        width: 0,
        height: 1,
      },
      shadowOpacity: 0.90,
      shadowRadius: 9.46,
      overflow: 'visible'
    },
    pressText: {
      marginTop: '30%',
      color: '#FFFFFF',
      fontSize: 30,
      
    },
    joke:{
      color: '#36cecc',
      fontSize: 15,
      marginTop: '45%',
      marginLeft: 40,
      marginRight: 40,
      textAlign: 'center',
      
     }

  });