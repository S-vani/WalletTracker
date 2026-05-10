import { useEffect } from "react";
import { useSearchParams } from "react-router-dom";
import {verify} from "../services/api"

function VerifyPage() {
    const [params] = useSearchParams();

    useEffect(() => {
        verify(params);

    }, []);

    return(
        <h1>
            Verifying...
        </h1>
    )
}

export default VerifyPage;
