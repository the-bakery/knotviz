
module VQM where

data Vec3 s = Vec3 s s s
              deriving (Eq, Show)

instance Functor Vec3 where
    fmap = vFMap

data Quat s = Quat s (Vec3 s)
              deriving (Eq, Show)

instance Functor Quat where
    fmap = qFMap

data M3x3 s = M3x3 (Vec3 s) (Vec3 s) (Vec3 s)
              deriving (Eq, Show)

instance Functor M3x3 where
    fmap = mFMap

zero :: (Num s) => s
zero = fromInteger 0

one :: (Num s) => s
one = fromInteger 1

vZipWith :: (s -> t -> u) -> Vec3 s -> Vec3 t -> Vec3 u
vZipWith f (Vec3 ax ay az) (Vec3 bx by bz) = Vec3 (f ax bx) (f ay by) (f az bz)

vFMap :: (s -> t) -> Vec3 s -> Vec3 t
vFMap f (Vec3 x y z) = Vec3 (f x) (f y) (f z)

vScale :: (Num s) => s -> Vec3 s -> Vec3 s
vScale s = vFMap (s*)

vNeg :: (Num s) => Vec3 s -> Vec3 s
vNeg = vFMap negate

vAdd :: (Num s) => Vec3 s -> Vec3 s -> Vec3 s
vAdd = vZipWith (+)

vSub :: (Num s) => Vec3 s -> Vec3 s -> Vec3 s
vSub = vZipWith (-)

vCross :: (Num s) => Vec3 s -> Vec3 s -> Vec3 s
vCross (Vec3 ax ay az) (Vec3 bx by bz) =
    Vec3
    (ay*bz - az*by)
    (az*bx - ax*bz)
    (ax*by - ay*bx)

vDot :: (Num s) => Vec3 s -> Vec3 s -> s
vDot (Vec3 ax ay az) (Vec3 bx by bz) = ax*bx + ay*by + az*bz

vNormSq :: (Num s) => Vec3 s -> s
vNormSq v = vDot v v

vNorm :: (Floating s) => Vec3 s -> s
vNorm v = sqrt (vNormSq v)

vNormUnit :: (Eq s, Floating s) => Vec3 s -> Maybe (s, Vec3 s)
vNormUnit v =
    let n = vNorm v in
    if n == zero then Nothing else Just (n, vScale (recip n) v)

vUnit :: (Eq s, Floating s) => Vec3 s -> Maybe (Vec3 s)
vUnit v =
    case (vNormUnit v) of
      Nothing -> Nothing
      Just (_, u) -> Just u

vToQuat :: (Eq s, Floating s) => Vec3 s -> Quat s
vToQuat v =
    case (vNormUnit v) of
      Nothing -> Quat one (Vec3 zero zero zero)
      Just (n, u) -> Quat (cos n) (vScale (sin n) u)

qFMap :: (s -> t) -> Quat s -> Quat t
qFMap f (Quat w v) = Quat (f w) (vFMap f v)

qScale :: (Num s) => s -> Quat s -> Quat s
qScale s = qFMap (s*)

qConj :: (Num s) => Quat s -> Quat s
qConj (Quat w v) = Quat w (vNeg v)

qNeg :: (Num s) => Quat s -> Quat s
qNeg = qFMap negate

qMul :: (Num s) => Quat s -> Quat s -> Quat s
qMul (Quat aw av) (Quat bw bv) =
    Quat
    (aw*bw - vDot av bv)
    (vAdd (vAdd (vScale aw bv) (vScale bw av)) (vCross av bv))

qDot :: (Num s) => Quat s -> Quat s -> s
qDot (Quat aw av) (Quat bw bv) = aw*bw + vDot av bv

qNormSq :: (Num s) => Quat s -> s
qNormSq q = qDot q q

qNorm :: (Floating s) => Quat s -> s
qNorm q = sqrt (qNormSq q)

qNormUnit :: (Eq s, Floating s) => Quat s -> Maybe (s, Quat s)
qNormUnit q =
    let n = qNorm q in
    if n == zero then Nothing else Just (n, qScale (recip n) q)

qUnit :: (Eq s, Floating s) => Quat s -> Maybe (Quat s)
qUnit q =
    case (qNormUnit q) of
      Nothing -> Nothing
      Just (_, u) -> Just u

qInv :: (Eq s, Fractional s) => Quat s -> Maybe (Quat s)
qInv q =
    let nn = qNormSq q in
    if nn == zero
    then Nothing
    else Just (qScale (recip nn) (qConj q))

qToM3x3 :: (Num s) => Quat s -> M3x3 s
qToM3x3 (Quat w (Vec3 x y z)) =
    let dbl a = a + a in
    M3x3
    ( Vec3 (w*w+x*x-y*y-z*z) (dbl (x*y + w*z)) (dbl (x*z - w*y)) )
    ( Vec3 (dbl (x*y - w*z)) (w*w-x*x+y*y-z*z) (dbl (y*z + w*x)) )
    ( Vec3 (dbl (x*z + w*y)) (dbl (y*z - w*x)) (w*w-x*x-y*y+z*z) )

mCMap :: (Vec3 s -> Vec3 t) -> M3x3 s -> M3x3 t
mCMap f (M3x3 i j k) = M3x3 (f i) (f j) (f k)

mFMap :: (s -> t) -> M3x3 s -> M3x3 t
mFMap f = mCMap (vFMap f)

mScale :: (Num s) => s -> M3x3 s -> M3x3 s
mScale s = mFMap (s*)

mZipWith :: (s -> t -> u) -> M3x3 s -> M3x3 t -> M3x3 u
mZipWith f (M3x3 ai aj ak) (M3x3 bi bj bk) =
    M3x3
    (vZipWith f ai bi) (vZipWith f aj bj) (vZipWith f ak bk)

mNeg :: (Num s) => M3x3 s -> M3x3 s
mNeg = mCMap vNeg

mAdd :: (Num s) => M3x3 s -> M3x3 s -> M3x3 s
mAdd = mZipWith (+)

mSub :: (Num s) => M3x3 s -> M3x3 s -> M3x3 s
mSub = mZipWith (-)

mApp :: (Num s) => M3x3 s -> Vec3 s -> Vec3 s
mApp (M3x3 i j k) (Vec3 x y z) =
    vAdd (vAdd (vScale x i) (vScale y j)) (vScale z k)

mMul :: (Num s) => M3x3 s -> M3x3 s -> M3x3 s
mMul a b = mCMap (mApp a) b
