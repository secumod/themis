/**
 * @file
 *
 * Created by Andrey Mnatsakanov on 03/18/2015
 * (c) CossackLabs
 */

#import <Foundation/Foundation.h>
#import <themis/themis.h>

@interface SCell_seal : NSObject
{
  NSData* key_;
}

- (id)init: (NSData*)key;
- (NSData*)wrap: (NSData*)message;
- (NSData*)unwrap: (NSData*)message;
- (NSData*)wrap: (NSData*)message context:(NSData*)contex;
- (NSData*)unwrap: (NSData*)message context:(NSData*)contex;

@end
