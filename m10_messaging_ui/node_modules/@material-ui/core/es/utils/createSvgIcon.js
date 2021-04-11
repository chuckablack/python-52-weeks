import _extends from "@babel/runtime/helpers/esm/extends";
import React from 'react';
import SvgIcon from '../SvgIcon';
/**
 * Private module reserved for @material-ui/x packages.
 */

export default function createSvgIcon(path, displayName) {
  const Component = React.memo(React.forwardRef((props, ref) => /*#__PURE__*/React.createElement(SvgIcon, _extends({
    ref: ref
  }, props), path)));

  if (process.env.NODE_ENV !== 'production') {
    Component.displayName = `${displayName}Icon`;
  }

  Component.muiName = SvgIcon.muiName;
  return Component;
}