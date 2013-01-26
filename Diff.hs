
module Diff where

data Dual a = Join a (Dual a)

diffF :: (Functor f) => f (Dual a) -> f (Dual a)
diffF = fmap diff

primalF :: (Functor f) => f (Dual a) -> f a
primalF = fmap primal

dualF :: (Functor f, Num a) => f a -> f (Dual a)
dualF = fmap dual

diff :: Dual a -> Dual a
diff (Join _ t) = t

primal :: Dual a -> a
primal (Join v _) = v

integrate :: a -> Dual a -> Dual a
integrate = Join

dual :: (Num a) => a -> Dual a
dual x = integrate x one

zero :: (Num a) => Dual a
zero = integrate (fromInteger 0) zero

lift :: (Num a) => a -> Dual a
lift x = integrate x zero

one :: (Num a) => Dual a
one = integrate (fromInteger 1) zero

instance (Eq a) => Eq (Dual a) where
    x == y  =  primal x == primal y

instance (Eq a, Num a) => Num (Dual a) where
    x + y  =  integrate (primal x + primal y) (diff x + diff y)
    x * y  =  integrate (primal x * primal y) (diff x * y + x * diff y)
    negate x  =  integrate (negate $ primal x) (negate $ diff x)
    abs x  =  if primal x == 0
              then error "can't differentiate abs(x) in x = 0"
              else integrate (abs $ primal x) (diff x * signum x)
    signum x  =  if primal x == 0
                 then error "can't differentiate signum(x) in x = 0"
                 else integrate (signum $ primal x) zero
    fromInteger x  =  integrate (fromInteger x) zero

instance (Eq a, Fractional a) => Fractional (Dual a) where
    recip x  =  integrate (recip $ primal x) (-diff x / x^2)
    fromRational x  =  integrate (fromRational x) zero

instance (Eq a, Floating a) => Floating (Dual a) where
    pi  =  integrate pi zero
    exp x  =  integrate (exp $ primal x) (diff x * exp x)
    sqrt x  =  integrate (sqrt $ primal x) (diff x / (2 * sqrt x))
    log x  =  integrate (log $ primal x) (diff x / x)
    sin x  =  integrate (sin $ primal x) ( diff x * cos x)
    cos x  =  integrate (cos $ primal x) (-diff x * sin x)
    sinh x  =  integrate (sinh $ primal x) (diff x * cosh x)
    cosh x  =  integrate (cosh $ primal x) (diff x * sinh x)
    asin x  =  integrate (asin $ primal x) ( diff x / sqrt (1 - x^2))
    acos x  =  integrate (acos $ primal x) (-diff x / sqrt (1 - x^2))
    atan x  =  integrate (atan $ primal x) (diff x / (1 + x^2))
    asinh x  =  integrate (asinh $ primal x) (diff x / sqrt (x^2 + 1))
    acosh x  =  integrate (acosh $ primal x) (diff x / sqrt (x^2 - 1))
    atanh x  =  integrate (atanh $ primal x) (diff x / (1 - x^2))
