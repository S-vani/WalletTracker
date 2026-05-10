import LoginForm from "../Authentication/LoginForm.jsx";
import {loginAuthentication} from "../services/api";

function LoginPage() {

    const test = async () => {
        console.log("closed")
    }

    return (
        <LoginForm onClose={test} onSubmit={loginAuthentication}/>
    )
}

export default LoginPage
