import {Fragment, useEffect, useRef, useState} from "react"
import {useRouter} from "next/router"
import {E, connect, isTrue, set_val, updateState, uploadFiles} from "/utils/state"
import "focus-visible/dist/focus-visible"
import {Alert, AlertIcon, AlertTitle, Avatar, Box, Button, Center, CircularProgress, Container, Grid, GridItem, HStack, Heading, Input, Link, Menu, MenuButton, MenuDivider, MenuItem, MenuList, SkeletonText, Spacer, Text, VStack, useColorMode} from "@chakra-ui/react"
import NextLink from "next/link"
import NextHead from "next/head"

const PING = "http://localhost:8000/ping"
const EVENT = "ws://localhost:8000/event"
const UPLOAD = "http://localhost:8000/upload"
export default function Component() {
const [state, setState] = useState({"api_keystate": "info", "check_is_login": false, "is_hydrated": false, "logged_in": false, "openai_apikey": "", "openai_apikey_value": "", "retrieve_api_keystate": "info", "search_loading": false, "search_text": "", "summarize_loading": true, "summary_text": "", "text": "", "titles": [], "username": "", "events": [{"name": "state.hydrate"}], "files": []})
const [result, setResult] = useState({"state": null, "events": [], "processing": false})
const router = useRouter()
const socket = useRef(null)
const { isReady } = router;
const { colorMode, toggleColorMode } = useColorMode()
const Event = events => setState({
  ...state,
  events: [...state.events, ...events],
})
const File = files => setState({
  ...state,
  files,
})
useEffect(() => {
  if(!isReady) {
    return;
  }
  if (!socket.current) {
    connect(socket, state, setState, result, setResult, router, EVENT, ['websocket', 'polling'])
  }
  const update = async () => {
    if (result.state != null) {
      setState({
        ...result.state,
        events: [...state.events, ...result.events],
      })
      setResult({
        state: null,
        events: [],
        processing: false,
      })
    }
    await updateState(state, setState, result, setResult, router, socket.current)
  }
  update()
})

return (
<VStack><Box sx={{"position": "fixed", "width": "70%", "top": "0px", "zIndex": "500", "marginTop": "20px"}}><HStack alignItems="center"
sx={{"border": "0.2em solid rgba(0,0,0,0.5)", "paddingX": "2em", "paddingY": "0.5em", "borderRadius": "20px"}}><NextLink href="/"
passHref={true}><Link><Heading onClick={() => Event([E("state.clear_history", {})])}
sx={{"fontSize": "1.75em"}}>{`NewsGPT`}</Heading></Link></NextLink>
<Spacer/>
<HStack><Input onChange={(_e) => Event([E("state.set_text", {text:_e.target.value})])}
placeholder="New Topic?"
sx={{"borderRadius": "20px", "width": "400px"}}
type="text"
value={state.text}/>
<Button isActive={true}
onClick={() => Event([E("state.search_process", {}),E("state.search", {}),E("state.search_process", {})])}
size="sm"
sx={{"bg": "lightgreen", "color": "black", "borderRadius": "1em", "_hover": {"opacity": 0.6}}}
variant="outline">{`Search`}</Button></HStack>
<Spacer/>
<Menu><Fragment>{isTrue(state.check_is_login) ? <Fragment><MenuButton><Avatar name={state.username}
size="md"/></MenuButton></Fragment> : <Fragment><MenuButton sx={{"marginRight": "30px", "borderRadius": "1em", "_hover": {"opacity": 0.6}, "width": "100px", "height": "30px", "color": "black", "background": "rgba(0,0,0,0.1)"}}>{`Login`}</MenuButton></Fragment>}</Fragment>
<MenuList><Fragment>{isTrue(state.check_is_login) ? <Fragment><VStack><Center><VStack><Avatar name={state.username}
size="md"/>
<Text>{state.username}</Text></VStack></Center>
<MenuDivider/>
<NextLink href="#"
passHref={true}><Link onClick={() => Event([E("state.logout", {})])}><MenuItem>{`Sign Out`}</MenuItem></Link></NextLink></VStack></Fragment> : <Fragment><VStack alignItems="center"><Input onBlur={(_e) => Event([E("state.set_username", {text:_e.target.value})])}
placeholder="username"
sx={{"borderRadius": "10px", "width": "80%"}}
type="text"/>
<Input onBlur={(_e) => Event([E("state.set_openai_temp_key", {key:_e.target.value})])}
placeholder="openai api-key"
sx={{"borderRadius": "10px", "width": "80%"}}
type="password"/>
<Alert status={state.retrieve_api_keystate}><AlertIcon/>
<AlertTitle>{("openai key status: " + state.retrieve_api_keystate)}</AlertTitle></Alert>
<Button isActive={true}
onClick={() => Event([E("state.on_check_apikey", {}),E("state.clear_history", {})])}
size="sm"
sx={{"bg": "lightgreen", "color": "black", "borderRadius": "1em", "_hover": {"opacity": 0.6}}}
variant="outline">{`Submit`}</Button></VStack></Fragment>}</Fragment></MenuList></Menu></HStack></Box>
<Grid sx={{"width": "100%"}}
templateColumns="repeat(8, 1fr)"
templateRows="repeat(5, 1fr)"><GridItem colSpan={1}
rowSpan={5}><Spacer/></GridItem>
<Fragment>{isTrue(state.search_loading) ? <Fragment><CircularProgress isIndeterminate={true}
sx={{"position": "absolute", "top": "50%", "left": "30%"}}/></Fragment> : <Fragment><GridItem colSpan={3}
rowSpan={5}
sx={{"marginTop": "10em", "borderRadius": "20px", "boxShadow": "7px -7px 14px #cccecf, -7px 7px 14px #ffffff"}}><VStack sx={{"overflow": "auto", "height": "750px"}}>{state.titles.map((dtjvzcgf, i) => <Container key={i}><Box onClick={() => Event([E("state.summarize_process", {}),E("state.summarize", {title:dtjvzcgf}),E("state.summarize_process", {})])}
sx={{"bg": "rgba(255,255,255, 0.5)", "boxShadow": "3px -3px 7px #cccecf, -3px 3px 7px #ffffff", "borderRadius": "10px", "height": "80px", "width": "100%", "marginTop": "0.75em", "alignItems": "left", "_hover": {"cursor": "pointer"}}}><Text sx={{"padding": "1em", "fontWeight": "bold", "fontSize": "0.9em"}}>{dtjvzcgf}</Text></Box></Container>)}</VStack></GridItem></Fragment>}</Fragment>
<GridItem colSpan={3}
rowSpan={5}
sx={{"marginTop": "10em", "borderRadius": "20px", "marginLeft": "50px", "boxShadow": "7px -7px 14px #cccecf, -7px 7px 14px #ffffff", "overflow": "auto", "height": "750px"}}><SkeletonText endColor="orange.500"
isLoaded={state.summarize_loading}
noOfLines={5}
startColor="pink.500"
sx={{"padding": "3em"}}><Box dangerouslySetInnerHTML={{"__html": state.summary_text}}
sx={{"padding": "3em"}}/></SkeletonText></GridItem></Grid>
<NextHead><title>{`Pynecone App`}</title>
<meta content="A Pynecone app."
name="description"/>
<meta content="favicon.ico"
property="og:image"/></NextHead></VStack>
)
}