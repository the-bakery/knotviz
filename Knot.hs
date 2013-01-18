
module Knot where

import VQM

type Curve s = s -> Vec3 s

sampleCurve :: (Fractional s) => Integer -> Curve s -> [Vec3 s]
sampleCurve n curve =
    map curve [fromInteger i / fromInteger n | i <- [0..n]]

torusKnot :: (Floating s) => Integer -> Integer -> Curve s
torusKnot p q t =
    let two = fromInteger 2
        w = two * pi * t
        p' = w * fromInteger p
        q' = w * fromInteger q
        r = cos q' + two
    in
    Vec3
    (r * cos p')
    (r * sin p')
    (-sin q')
