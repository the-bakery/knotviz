
module Main where

import Control.Monad
import Data.Array.IArray
import Data.IORef
import Data.Ix
import Graphics.UI.GLUT
import System.Exit

import VQM
import Knot

main :: IO ()
main = do
  (name, args) <- getArgsAndInitialize
  {-
  when (args==[]) $ do
         printHelp name
         exitFailure
  -}
  initialWindowSize $= Size 800 600
  initialDisplayMode $= [RGBMode, DoubleBuffered, WithDepthBuffer]
  createWindow "knotviz"
  state <- makeState args
  displayCallback $= displayAction state
  reshapeCallback $= Just (reshapeAction state)
  keyboardMouseCallback $= Just (keyboardMouseAction state)
  passiveMotionCallback $= Just (passiveMotionAction state)
  motionCallback $= Just (activeMotionAction state)
  depthFunc $= Just Less
  mainLoop

data State = State {
      prevPtrPos :: IORef Position,
      orientation :: IORef (Quat GLdouble),
      leftButton :: IORef Bool
    }

makeState :: [String] -> IO State
makeState args = do
  i_ori <- newIORef (Quat 1.0 (Vec3 0.0 0.0 0.0))
  i_pos <- newIORef (Position 0 0)
  i_ltb <- newIORef False
  return $ State {
               orientation = i_ori,
               prevPtrPos = i_pos,
               leftButton = i_ltb
             }

glCurveVert :: (VertexComponent s, TexCoordComponent s) => CurveVert s -> IO ()
glCurveVert (Vec3 x y z, t) = do
  texCoord (TexCoord1 t)
  vertex (Vertex3 x y z)

glPatchVert :: (VertexComponent s, NormalComponent s, TexCoordComponent s) => PatchVert s -> IO ()
glPatchVert (Vec3 x y z, Vec3 nx ny nz, t, u) = do
  texCoord (TexCoord2 t u)
  normal (Normal3 nx ny nz)
  vertex (Vertex3 x y z)

renderPolyLine :: PolyLine GLdouble -> IO ()
renderPolyLine vs = do
  renderPrimitive LineStrip $ mapM_ glCurveVert $ elems vs

renderPolyQuad :: PolyQuad GLdouble -> IO ()
renderPolyQuad vs = do
  let ((0,0),(n,m)) = bounds vs
  renderPrimitive Quads $ mapM_ glPatchVert $ map (vs !) $ concat $
    [[(i,j),(i+1,j),(i+1,j+1),(i,j+1)] | (i,j) <- range ((0,0),(n-1,m-1))]

curve :: PolyLine GLdouble
curve = sampleCurve 1024 $ torusCurve 3 5

patch :: PolyQuad GLdouble
--patch = samplePatch 64 32 $ torusPatch 2.0 0.8
--patch = samplePatch 256 16 $ curveTubePatch (torusCurve 3 5) 0.5
patch = samplePatch 256 4 $ curveRibbonPatch (torusCurve 3 5) 0.3

displayAction :: State -> DisplayCallback
displayAction state = do
  clearColor $= Color4 0.0 0.0 0.0 1.0
  clearDepth $= 1.0
  clear [ColorBuffer, DepthBuffer]
  matrixMode $= (Modelview 0)
  loadIdentity

  shadeModel $= Smooth
  normalize $= Enabled
  ambient (Light 0) $= Color4 0.1 0.1 0.1 1.0
  diffuse (Light 0) $= Color4 0.9 0.9 0.9 1.0
  position (Light 0) $= Vertex4 0.5 (-1.0) 0.5 0.0
  light (Light 0) $= Enabled

  ori <- get (orientation state)
  let (M3x3 (Vec3 ix iy iz) (Vec3 jx jy jz) (Vec3 kx ky kz)) = qToM3x3 ori
  rot <- (newMatrix ColumnMajor [ix, iy, iz, 0.0,
                                 jx, jy, jz, 0.0,
                                 kx, ky, kz, 0.0,
                                 0.0, 0.0, 0.0, 1.0]) :: IO (GLmatrix GLdouble)
  translate (Vector3 0.0 0.0 (-4.0) :: Vector3 GLdouble)
  multMatrix rot

  lighting $= Disabled
  renderPolyLine curve

  --lighting $= Enabled
  --polygonMode $= (Fill, Fill)
  polygonMode $= (Line, Line)
  renderPolyQuad patch

  flush
  swapBuffers

keyboardMouseAction :: State -> KeyboardMouseCallback
keyboardMouseAction state key keyState mods _ = do
  postRedisplay Nothing
  case (key, keyState) of
    (MouseButton LeftButton, Down) -> leftButton state $= True
    (MouseButton LeftButton, Up) ->  leftButton state $= False
    --(SpecialKey KeyF5, Down) -> loadFunction state
    (_, _) -> return ()

passiveMotionAction :: State -> MotionCallback
passiveMotionAction state pos = do
  prevPtrPos state $= pos

activeMotionAction :: State -> MotionCallback
activeMotionAction state pos@(Position x y) = do
  ltb <- get (leftButton state)
  when ltb $ do
    postRedisplay Nothing
    Position px py <- get (prevPtrPos state)
    let d = Vec3 (fromIntegral (py - y)) (fromIntegral (x - px)) 0.0
    ori <- get (orientation state)
    let Just ori' = qUnit (qMul (vToQuat (vScale 0.002 d)) ori)
    orientation state $= ori'
  prevPtrPos state $= pos

{-
timerAction :: State -> TimerCallback
timerAction state = do
   rot <- get (shouldRotate state)
   when rot $ do
      ia <- get (inertia state)
      diff state $~ ($+ ia)
      postRedisplay Nothing
   addTimerCallback timerFrequencyMillis (timer state)
-}

reshapeAction :: State -> ReshapeCallback
reshapeAction state size@(Size w h) = do
  viewport $= (Position 0 0, size)
  -- plotSize state $= Vector2 (fromIntegral w) (fromIntegral h)
  matrixMode $= Projection
  loadIdentity
  let a = (fromIntegral w) / (fromIntegral h)
  let f = 0.001
  frustum (-a * f) (a * f) f (-f) f 100.0

printHelp :: String -> IO ()
printHelp name = mapM_ putStrLn [
  "Usage:",
  "",
  "  " ++ name ++ " [OPTIONS] INPUT",
  "",
  "Options:",
  "",
  "  -display DISPLAY",
  "    Specify the X server to connect to. If not specified,",
  "    the value of the DISPLAY environment variable is used.",
  "",
  "  -geometry WxH+X+Y",
  "    Determines where the window should be created on the screen.",
  "    The parameter should be formatted as a standard X geometry specification.",
  "",
  "  -iconic",
  "    Start minimized.",
  "",
  "  -indirect",
  "    Force indirect OpenGL rendering contexts.",
  "",
  "  -direct",
  "    Force direct OpenGL rendering contexts.",
  "",
  "  -gldebug",
  "    Helpful in detecting OpenGL run-time errors.",
  "",
  "  -sync",
  "    Enable synchronous X protocol transactions.",
  ""]
