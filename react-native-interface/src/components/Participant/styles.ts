import { StyleSheet } from "react-native";

export const styles = StyleSheet.create({
    container: {
        width: '100%',
        backgroundColor: "#86a1b8",
        borderRadius: 5,
        flexDirection: 'row',
        alignItems: 'center',
        marginBottom: 10
    },
    name: {
        color: "#FFFFFF",
        fontSize: 20,
        marginLeft: 16,
        flex: 1,
    },
    buttomText: {
        color: '#FFFFFF',
        fontSize: 20
    },
    buttom: {
        width: 56,
        height: 56,
        borderRadius: 5,
        backgroundColor: '#E23C44',
        alignItems: 'center',
        justifyContent: 'center'
    }
});