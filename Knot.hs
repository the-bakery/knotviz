
module Knot where

import Data.Array.IArray

import Diff
import VQM

type Curve s = s -> Vec3 s
type Patch s = s -> s -> Vec3 s

type CurveVert s = (Vec3 s, s)
type PatchVert s = (Vec3 s, Vec3 s, s, s)

type PolyLine s = Array Integer (CurveVert s)
type PolyQuad s = Array (Integer, Integer) (PatchVert s)

normalF :: (Fractional s) => Patch (Dual s) -> Patch s
normalF patch t u =
    let dfdt = primalF $ diffF $ patch (dual t) (lift u)
        dfdu = primalF $ diffF $ patch (lift t) (dual u)
    in vCross dfdu dfdt

sampleUnit :: (Fractional s) => Integer -> [s]
sampleUnit n = [fromInteger i / fromInteger n | i <- [0..n]]

sampleCurve :: (Fractional s) => Integer -> Curve (Dual s) -> PolyLine s
sampleCurve n curve =
    listArray (0,n) [evalCurve curve t | t <- sampleUnit n]

samplePatch :: (Fractional s) => Integer -> Integer -> Patch (Dual s) -> PolyQuad s
samplePatch n m patch =
    listArray ((0,0),(n,m)) [evalPatch patch t u
                                 | t <- sampleUnit n, u <- sampleUnit m]

evalCurve :: (Fractional s) => Curve (Dual s) -> s -> CurveVert s
evalCurve curve t =
    let pos = primalF $ curve (dual t)
    in (pos, t)

evalPatch :: (Fractional s) => Patch (Dual s) -> s -> s -> PatchVert s
evalPatch patch t u =
    let pos = primalF $ patch (dual t) (dual u)
        nrm = normalF patch t u
    in (pos, nrm, t, u)

ringCurve :: (Floating s) => s -> Curve s
ringCurve r t =
    let t' = 2 * pi * t
    in vScale r (Vec3 (cos t') (sin t') 0)

torusPatch :: (Floating s) => s -> s -> Patch s
torusPatch r1 r2 t u =
    let t' = 2 * pi * t
        u' = 2 * pi * u
        i = Vec3 (cos t') (sin t') 0
        j = Vec3 0 0 (-1)
        x = r2 * cos u' + r1
        y = r2 * sin u'
    in
    vAdd (vScale x i) (vScale y j)

torusCurve :: (Floating s) => Integer -> Integer -> Curve s
torusCurve p q t =
    let w = 2 * pi * t
        p' = w * fromInteger p
        q' = w * fromInteger q
        r = cos q' + 2
    in
    Vec3
    (r * cos p')
    (r * sin p')
    (-sin q')
