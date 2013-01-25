
module Knot where

import Data.Array.IArray

import VQM

type Curve s = s -> Vec3 s
type Patch s = s -> s -> Vec3 s

type PolyLine s = Array Integer (Vec3 s)
type PolyQuad s = Array (Integer, Integer) (Vec3 s)

sampleUnit :: (Fractional s) => Integer -> [s]
sampleUnit n = [fromInteger i / fromInteger n | i <- [0..n]]

sampleCurve :: (Fractional s) => Integer -> Curve s -> PolyLine s
sampleCurve n curve =
    listArray (0,n) [curve t | t <- sampleUnit n]

samplePatch :: (Fractional s) => Integer -> Integer -> Patch s -> PolyQuad s
samplePatch n m patch =
    listArray ((0,0),(n,m)) [patch t u | t <- sampleUnit n, u <- sampleUnit m]

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
