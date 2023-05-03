import {Head, Html, Main, NextScript} from "next/document"
import {ColorModeScript} from "@chakra-ui/react"
export default function Document() {
return (
<Html><Head><link href="https://fonts.googleapis.com/css2?family=Silkscreen&display=swap"
rel="stylesheet"/></Head>
<body><ColorModeScript initialColorMode="light"/>
<Main/>
<NextScript/></body></Html>
)
}